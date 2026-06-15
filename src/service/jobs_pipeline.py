import sqlite3
import datetime
from src.repository import DB_FILE

class JobsPipeline:
    def __init__(self, db_path: str = DB_FILE):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def check_job_exists(self, job_number: int, year: str) -> bool:
        """
        Check if a job already exists for a given number and year.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM tb_jobs 
            WHERE job_number = ? AND strftime('%Y', date_creation) = ?
        """, (job_number, year))
        row = cursor.fetchone()
        conn.close()
        return row is not None

    def create_job(self, job_data: dict) -> int:
        """
        Equivalent to create_update_job.php creation scenario.
        Creates records in tb_jobs, tb_jobs_dates, tb_jobs_date_install, and tb_jobs_details.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        job_number = job_data.get("job_number")
        date_creation = job_data.get("date_creation", datetime.date.today().strftime("%Y-%m-%d"))
        year = date_creation[:4]
        
        if self.check_job_exists(job_number, year):
            conn.close()
            raise ValueError(f"Job {job_number} already exists for year {year}")

        todays_date = datetime.date.today().strftime("%Y-%m-%d")

        # 1. Insert into tb_jobs
        cursor.execute("""
            INSERT INTO tb_jobs (
                date_creation, job_number, company, address, superlot, lot_group,
                site_supervisor_id, invoice_number, date_install, comment, completed,
                drawing_link, closed, approved_by, archived_by, date_archive, date_sign,
                archive_id, archive_comment
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            date_creation, job_number, job_data.get("company"), job_data.get("address"),
            job_data.get("superlot", ""), job_data.get("lot_group", ""),
            job_data.get("site_supervisor_id", 0), job_data.get("invoice_number", ""),
            job_data.get("date_install", ""), job_data.get("comment", ""), "0",
            job_data.get("drawing_link", ""), 0, "", "", "", "", 0, ""
        ))
        job_id = cursor.lastrowid

        # 2. Insert into tb_jobs_dates
        cursor.execute("""
            INSERT INTO tb_jobs_dates (job_id, year) VALUES (?, ?)
        """, (job_number, year))

        # 3. Insert initial lot 0 install status
        cursor.execute("""
            INSERT INTO tb_jobs_date_install (date_creation, job_number, active_flag, date_install, status)
            VALUES (?, ?, '0', NULL, 'design')
        """, (date_creation, job_number))

        # 4. Insert pages/items
        pages = job_data.get("pages", [])
        for page in pages:
            page_no = page.get("page")
            lot = page.get("lot")
            member = page.get("member")
            gp = 1 if page.get("gp") else 0
            q_det = page.get("q_det", 0.0)
            q_fab = page.get("q_fab", 0.0)
            q_inst = page.get("q_inst", 0.0)
            q_tr = page.get("q_tr", 0.0)

            if not lot or not member:
                continue

            # Check if Task/NCR/RFI
            is_task_special = any(member.lower().startswith(x) for x in ["task", "ncr", "rfi"])
            init_val = 1 if is_task_special else 0

            # Insert into tb_jobs_details (29 fields)
            cursor.execute(f"""
                INSERT INTO tb_jobs_details VALUES (
                    NULL, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?
                )
            """, (
                date_creation, job_number, page_no, lot, member,
                str(gp), str(q_det), str(q_fab), str(q_inst), str(q_tr),
                str(init_val), todays_date, str(init_val), todays_date,
                str(init_val), todays_date, str(init_val), todays_date,
                str(init_val), todays_date, str(init_val), todays_date,
                str(init_val), todays_date, "0", todays_date, "", ""
            ))
            # Insert into tb_wip. Let's insert into tb_wip matching SQLite schema in repository.py:
            # id, job_number, process_name, supervisor, status_flags, info, auditor, audit_flags, audit_info, date_audited, completed_flag, rev_no, date_rev, note
            cursor.execute("""
                INSERT INTO tb_wip (job_number, process_name, supervisor, auditor, completed_flag)
                VALUES (?, 'PE GMAW 02, PE GMAW 03, PE GMAW 04', 'Matt Leitch', 'Weldtest Paul', '0')
            """, (str(job_number),))

            # Update tb_jobs_date_install with the real lot
            cursor.execute("""
                SELECT id FROM tb_jobs_date_install WHERE job_number = ? AND active_flag = ?
            """, (job_number, lot))
            if not cursor.fetchone():
                status_install = "temp installed" if is_task_special else "design"
                cursor.execute("""
                    INSERT INTO tb_jobs_date_install (date_creation, job_number, active_flag, date_install, status)
                    VALUES (?, ?, ?, NULL, ?)
                """, (date_creation, job_number, lot, status_install))

        # Delete lot 0 placeholder if valid pages exist
        if pages:
            cursor.execute("""
                DELETE FROM tb_jobs_date_install WHERE date_creation = ? AND job_number = ? AND active_flag = '0'
            """, (date_creation, job_number))

        conn.commit()
        conn.close()
        return job_id

    def update_job(self, job_number: int, year: str, job_data: dict) -> bool:
        """
        Equivalent to create_update_job.php update scenario.
        Updates tb_jobs, tb_jobs_details, tb_jobs_date_install, and tb_wip.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        date_creation = job_data.get("date_creation")
        todays_date = datetime.date.today().strftime("%Y-%m-%d")

        # 1. Update tb_jobs
        cursor.execute("""
            UPDATE tb_jobs
            SET date_creation = ?, company = ?, address = ?, superlot = ?, lot_group = ?,
                site_supervisor_id = ?, invoice_number = ?, date_install = ?, comment = ?
            WHERE job_number = ? AND strftime('%Y', date_creation) = ?
        """, (
            date_creation, job_data.get("company"), job_data.get("address"),
            job_data.get("superlot", ""), job_data.get("lot_group", ""),
            job_data.get("site_supervisor_id", 0), job_data.get("invoice_number", ""),
            job_data.get("date_install", ""), job_data.get("comment", ""),
            job_number, year
        ))

        # 2. Process Pages/Items update and delete
        pages = job_data.get("pages", [])
        # Get existing pages count from tb_jobs_details for this job
        cursor.execute("""
            SELECT id, active_flag FROM tb_jobs_details 
            WHERE job_number = ? AND strftime('%Y', date_creation) = ?
            ORDER BY id
        """, (job_number, year))
        existing_items = cursor.fetchall()
        
        # Mark page sequence logic
        page_to_follow = 1
        deleted_count = 0

        # We loop up to the maximum of existing or incoming pages
        max_len = max(len(existing_items), len(pages))
        for idx in range(max_len):
            if idx < len(existing_items):
                # We are updating or deleting an existing row
                detail_id = existing_items[idx][0]
                old_lot = existing_items[idx][1]

                if idx < len(pages):
                    # Update scenario
                    page_item = pages[idx]
                    lot = page_item.get("lot")
                    member = page_item.get("member")
                    gp = 1 if page_item.get("gp") else 0
                    q_det = page_item.get("q_det", 0.0)
                    q_fab = page_item.get("q_fab", 0.0)
                    q_inst = page_item.get("q_inst", 0.0)
                    q_tr = page_item.get("q_tr", 0.0)

                    if not lot or not member:
                        # Deletion requested by sending empty lot/member
                        cursor.execute("DELETE FROM tb_jobs_details WHERE id = ?", (detail_id,))
                        # Note: tb_wip does not contain tb_jobs_id, so we do not delete from it by tb_jobs_id here.
                        
                        # Check if any other page uses this lot
                        cursor.execute("""
                            SELECT count(id) FROM tb_jobs_details 
                            WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = ?
                        """, (job_number, year, old_lot))
                        if cursor.fetchone()[0] == 0:
                            cursor.execute("""
                                DELETE FROM tb_jobs_date_install 
                                WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = ?
                            """, (job_number, year, old_lot))
                        deleted_count += 1
                    else:
                        is_task_special = any(member.lower().startswith(x) for x in ["task", "ncr", "rfi"])
                        init_val = "1" if is_task_special else "0"

                        # Update tb_jobs_details
                        cursor.execute(f"""
                            UPDATE tb_jobs_details
                            SET item_number = ?, active_flag = ?, item_name = ?, c7 = ?, 
                                c8 = ?, c9 = ?, c10 = ?, c11 = ?
                            WHERE id = ?
                        """, (
                            str(page_to_follow), lot, member, str(gp), 
                            str(q_det), str(q_fab), str(q_inst), str(q_tr),
                            detail_id
                        ))

                        # Ensure wip exists
                        cursor.execute("SELECT id FROM tb_wip WHERE job_number = ?", (str(job_number),))
                        if not cursor.fetchone():
                            cursor.execute("""
                                INSERT INTO tb_wip (job_number, process_name, supervisor, auditor, completed_flag)
                                VALUES (?, 'PE GMAW 02, PE GMAW 03, PE GMAW 04', 'Matt Leitch', 'Weldtest Paul', '0')
                            """, (str(job_number),))

                        # Install date status check
                        cursor.execute("""
                            SELECT id FROM tb_jobs_date_install 
                            WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = ?
                        """, (job_number, year, lot))
                        if not cursor.fetchone():
                            status_install = "temp installed" if is_task_special else "design"
                            cursor.execute("""
                                INSERT INTO tb_jobs_date_install (date_creation, job_number, active_flag, date_install, status)
                                VALUES (?, ?, ?, NULL, ?)
                            """, (date_creation, job_number, lot, status_install))

                        # Delete old lot install status if no longer used
                        if old_lot != lot:
                            cursor.execute("""
                                SELECT count(id) FROM tb_jobs_details 
                                WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = ?
                            """, (job_number, year, old_lot))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("""
                                    DELETE FROM tb_jobs_date_install 
                                    WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = ?
                                """, (job_number, year, old_lot))
                        
                        page_to_follow += 1
                else:
                    # Extra existing records to delete (not in incoming request)
                    cursor.execute("DELETE FROM tb_jobs_details WHERE id = ?", (detail_id,))
                    # Note: We do not delete from tb_wip directly since it associates with job_number, not detail_id
                    cursor.execute("""
                        SELECT count(id) FROM tb_jobs_details 
                        WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = ?
                    """, (job_number, year, old_lot))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("""
                            DELETE FROM tb_jobs_date_install 
                            WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = ?
                        """, (job_number, year, old_lot))
            else:
                # Insert scenario (new page added in update request)
                page_item = pages[idx]
                lot = page_item.get("lot")
                member = page_item.get("member")
                gp = 1 if page_item.get("gp") else 0
                q_det = page_item.get("q_det", 0.0)
                q_fab = page_item.get("q_fab", 0.0)
                q_inst = page_item.get("q_inst", 0.0)
                q_tr = page_item.get("q_tr", 0.0)

                if lot and member:
                    is_task_special = any(member.lower().startswith(x) for x in ["task", "ncr", "rfi"])
                    init_val = 1 if is_task_special else 0

                    cursor.execute(f"""
                        INSERT INTO tb_jobs_details VALUES (
                            NULL, ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?,
                            ?, ?, ?, ?, ?,
                            ?, ?, ?
                        )
                    """, (
                        date_creation, job_number, str(page_to_follow), lot, member,
                        str(gp), str(q_det), str(q_fab), str(q_inst), str(q_tr),
                        str(init_val), todays_date, str(init_val), todays_date,
                        str(init_val), todays_date, str(init_val), todays_date,
                        str(init_val), todays_date, str(init_val), todays_date,
                        str(init_val), todays_date, "0", todays_date, "", ""
                    ))

                    cursor.execute("""
                        INSERT INTO tb_wip (job_number, process_name, supervisor, auditor, completed_flag)
                        VALUES (?, 'PE GMAW 02, PE GMAW 03, PE GMAW 04', 'Matt Leitch', 'Weldtest Paul', '0')
                    """, (str(job_number),))

                    cursor.execute("""
                        SELECT id FROM tb_jobs_date_install 
                        WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = ?
                    """, (job_number, year, lot))
                    if not cursor.fetchone():
                        status_install = "temp installed" if is_task_special else "design"
                        cursor.execute("""
                            INSERT INTO tb_jobs_date_install (date_creation, job_number, active_flag, date_install, status)
                            VALUES (?, ?, ?, NULL, ?)
                        """, (date_creation, job_number, lot, status_install))
                    
                    page_to_follow += 1

        # Delete lot 0 placeholder if valid pages exist
        cursor.execute("""
            SELECT count(id) FROM tb_jobs_details 
            WHERE job_number = ? AND strftime('%Y', date_creation) = ?
        """, (job_number, year))
        if cursor.fetchone()[0] > 0:
            cursor.execute("""
                DELETE FROM tb_jobs_date_install 
                WHERE job_number = ? AND strftime('%Y', date_creation) = ? AND active_flag = '0'
            """, (job_number, year))

        conn.commit()
        conn.close()
        return True

    def list_jobs(self) -> list:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, date_creation, job_number, company, address FROM tb_jobs ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "date_creation": r[1], "job_number": r[2], "company": r[3], "address": r[4]} for r in rows]

if __name__ == "__main__":
    print("Testing JobsPipeline Standalone CRUD...")
    pipeline = JobsPipeline()
    
    # Check current job count
    jobs_init = pipeline.list_jobs()
    print(f"Initial Jobs count: {len(jobs_init)}")
    
    # Dynamic unique job number based on current seconds
    import time
    dynamic_job_number = int(time.time()) % 100000
    
    mock_job = {
        "job_number": dynamic_job_number,
        "company": "Test standalone company",
        "address": "123 Standalone Road",
        "superlot": "Lot A",
        "date_creation": "2026-06-15",
        "pages": [
            {"page": "1", "lot": "L1", "member": "Beam 1", "gp": True, "q_det": 2.5},
            {"page": "2", "lot": "L2", "member": "TASK-Fix bolts", "gp": False, "q_inst": 1.0}
        ]
    }
    
    new_id = pipeline.create_job(mock_job)
    print(f"Success! Created Job ID: {new_id}")
    
    # Verify job list increased
    jobs_after = pipeline.list_jobs()
    print(f"New Jobs count: {len(jobs_after)}")
    assert len(jobs_after) == len(jobs_init) + 1
    
    # Test Update Scenario
    update_data = {
        "company": "Updated Company Name",
        "address": "456 Updated Lane",
        "superlot": "Lot B",
        "date_creation": "2026-06-15",
        "pages": [
            {"page": "1", "lot": "L1", "member": "Beam 1 - Rev1", "gp": True, "q_det": 3.0}, # update
            {"page": "2", "lot": "", "member": ""}, # delete
            {"page": "3", "lot": "L3", "member": "Column New", "gp": False} # insert
        ]
    }
    
    update_success = pipeline.update_job(dynamic_job_number, "2026", update_data)
    assert update_success is True
    print("JobsPipeline Update Standalone Test PASSED.")
    
    # Fetch details to verify
    conn = pipeline.get_connection()
    c = conn.cursor()
    c.execute("SELECT company, address FROM tb_jobs WHERE id = ?", (new_id,))
    job_row = c.fetchone()
    assert job_row[0] == "Updated Company Name"
    assert job_row[1] == "456 Updated Lane"
    
    c.execute("SELECT item_name, active_flag, item_number FROM tb_jobs_details WHERE job_number = ? ORDER BY id", (dynamic_job_number,))
    details = c.fetchall()
    print("Updated Job Details inside DB:", details)
    # Deleted the L2 TASK, updated L1 member, added L3 page. L1 is page 1, L3 is page 2
    assert len(details) == 2
    assert details[0][0] == "Beam 1 - Rev1"
    assert details[0][2] == "1"
    assert details[1][0] == "Column New"
    assert details[1][2] == "2"
    
    # Clean up test records
    c.execute("DELETE FROM tb_jobs WHERE job_number = ? AND strftime('%Y', date_creation) = '2026'", (dynamic_job_number,))
    c.execute("DELETE FROM tb_jobs_details WHERE job_number = ? AND strftime('%Y', date_creation) = '2026'", (dynamic_job_number,))
    c.execute("DELETE FROM tb_jobs_date_install WHERE job_number = ? AND strftime('%Y', date_creation) = '2026'", (dynamic_job_number,))
    c.execute("DELETE FROM tb_wip WHERE job_number = ?", (str(dynamic_job_number),))
    conn.commit()
    conn.close()
    print("JobsPipeline Standalone Test ALL PASSED (Cleaned up test data).")
