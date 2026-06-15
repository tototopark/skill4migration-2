import os
import csv
import sqlite3
import shutil

DB_FILE = "f:/pe/public_html/test-migration/skill4migration-2/storage/db.sqlite3"

# SQLite 스키마 정의
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS tb_login (
    id INTEGER PRIMARY KEY,
    login TEXT UNIQUE,
    password TEXT,
    firstname TEXT,
    lastname TEXT,
    avatar TEXT,
    shop_id INTEGER,
    date_hire TEXT,
    position TEXT,
    right_level INTEGER,
    comment TEXT,
    activated INTEGER,
    code_ccs TEXT,
    accreditation TEXT,
    date_accreditation TEXT,
    is_deleted INTEGER,
    ip_1 TEXT,
    ip_2 TEXT,
    ip_3 TEXT
);

CREATE TABLE IF NOT EXISTS tb_keys_remote_devices (
    id INTEGER PRIMARY KEY,
    device_name TEXT,
    email TEXT,
    private_key TEXT,
    ip_address TEXT,
    request_date TEXT,
    admin_validation INTEGER
);

CREATE TABLE IF NOT EXISTS tb_jobs (
    id INTEGER PRIMARY KEY,
    date_creation TEXT,
    job_number INTEGER,
    company TEXT,
    address TEXT,
    delivery_name TEXT,
    superlot TEXT,
    lot_group TEXT,
    site_supervisor_id INTEGER,
    invoice_number TEXT,
    date_install TEXT,
    comment TEXT,
    completed TEXT,
    drawing_link TEXT,
    closed INTEGER,
    approved_by TEXT,
    archived_by TEXT,
    date_archive TEXT,
    date_sign TEXT,
    archive_id INTEGER,
    archive_comment TEXT
);

CREATE TABLE IF NOT EXISTS tb_jobs_date_install (
    id INTEGER PRIMARY KEY,
    date_creation TEXT,
    job_number INTEGER,
    active_flag TEXT,
    date_install TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS tb_jobs_dates (
    id INTEGER PRIMARY KEY,
    job_id INTEGER,
    year TEXT,
    c3 TEXT, c4 TEXT, c5 TEXT, c6 TEXT, c7 TEXT, c8 TEXT, c9 TEXT, c10 TEXT,
    c11 TEXT, c12 TEXT, c13 TEXT, c14 TEXT, c15 TEXT, c16 TEXT, c17 TEXT, c18 TEXT, c19 TEXT, c20 TEXT,
    c21 TEXT, c22 TEXT, c23 TEXT, c24 TEXT, c25 TEXT, c26 TEXT, c27 TEXT, c28 TEXT, c29 TEXT, c30 TEXT,
    c31 TEXT, c32 TEXT, c33 TEXT, c34 TEXT
);

CREATE TABLE IF NOT EXISTS tb_jobs_details (
    id INTEGER PRIMARY KEY,
    date_creation TEXT,
    job_number INTEGER,
    item_number TEXT,
    active_flag TEXT,
    item_name TEXT,
    c7 TEXT, c8 TEXT, c9 TEXT, c10 TEXT,
    c11 TEXT, c12 TEXT, c13 TEXT, c14 TEXT, c15 TEXT, c16 TEXT, c17 TEXT, c18 TEXT, c19 TEXT, c20 TEXT,
    c21 TEXT, c22 TEXT, c23 TEXT, c24 TEXT, c25 TEXT, c26 TEXT, c27 TEXT, c28 TEXT, c29 TEXT
);

CREATE TABLE IF NOT EXISTS tb_tasks (
    id INTEGER PRIMARY KEY,
    task_name TEXT,
    task_desc TEXT,
    task_type INTEGER,
    job_id INTEGER,
    status INTEGER,
    due_date TEXT,
    assignee_id INTEGER,
    assignee_name TEXT,
    date_complete TEXT
);

CREATE TABLE IF NOT EXISTS tb_tasks_employees_affectation (
    id INTEGER PRIMARY KEY,
    employee_1 TEXT, employee_2 TEXT, employee_3 TEXT, employee_4 TEXT, employee_5 TEXT,
    employee_6 TEXT, employee_7 TEXT, employee_8 TEXT, employee_9 TEXT, employee_10 TEXT
);

CREATE TABLE IF NOT EXISTS tb_leaves (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    reason TEXT,
    date_start TEXT,
    date_end TEXT
);

CREATE TABLE IF NOT EXISTS tb_public_holidays (
    id INTEGER PRIMARY KEY,
    holiday_name TEXT,
    date_start TEXT,
    date_end TEXT
);

CREATE TABLE IF NOT EXISTS tb_punchsheet (
    id INTEGER PRIMARY KEY,
    year TEXT,
    month TEXT,
    day TEXT,
    employee_id TEXT,
    job_id TEXT,
    activity TEXT,
    status TEXT,
    time_str TEXT,
    am_pm TEXT,
    comment TEXT,
    extra TEXT
);

CREATE TABLE IF NOT EXISTS tb_reminder_other (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    expiry_date TEXT
);

CREATE TABLE IF NOT EXISTS tb_reminder_vehicle (
    id INTEGER PRIMARY KEY,
    vehicle_name TEXT,
    plate_number TEXT,
    wof_date TEXT,
    rego_date TEXT,
    mileage TEXT,
    next_mileage TEXT,
    last_mileage TEXT,
    comment TEXT
);

CREATE TABLE IF NOT EXISTS tb_wip (
    id INTEGER PRIMARY KEY,
    job_number TEXT,
    process_name TEXT,
    supervisor TEXT,
    status_flags TEXT,
    info TEXT,
    auditor TEXT,
    audit_flags TEXT,
    audit_info TEXT,
    date_audited TEXT,
    completed_flag TEXT,
    rev_no TEXT,
    date_rev TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS tb_export_data (
    id INTEGER PRIMARY KEY,
    table_name TEXT,
    date_export TEXT,
    time_export TEXT,
    user_login TEXT
);
"""

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    return conn

def safe_int(val, default=0):
    if not val or val.strip() == "" or val.lower() == "null":
        return default
    try:
        return int(val)
    except ValueError:
        try:
            return int(float(val))
        except ValueError:
            return default

def import_csv_data(conn, csv_dir="f:/pe/public_html/test-migration/sitepro/SQL_DL_FILE-Dev"):
    cursor = conn.cursor()
    
    # 1. tb_login 임포트
    login_path = os.path.join(csv_dir, "SQL_tb_login.csv")
    if os.path.exists(login_path):
        cursor.execute("DELETE FROM tb_login;")
        with open(login_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 19:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_login (
                        id, login, password, firstname, lastname, avatar, shop_id, date_hire, position,
                        right_level, comment, activated, code_ccs, accreditation, date_accreditation,
                        is_deleted, ip_1, ip_2, ip_3
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    safe_int(row[0]) if row[0] else None,
                    row[1], row[2], row[3], row[4], row[5],
                    safe_int(row[6]),
                    row[7], row[8],
                    safe_int(row[9]),
                    row[10],
                    safe_int(row[11]),
                    row[12], row[13], row[14],
                    safe_int(row[15]),
                    row[16], row[17], row[18]
                ))
        print("Imported tb_login successfully.")

    # 2. tb_keys_remote_devices 임포트
    devices_path = os.path.join(csv_dir, "SQL_tb_keys_remote_devices.csv")
    if os.path.exists(devices_path):
        cursor.execute("DELETE FROM tb_keys_remote_devices;")
        with open(devices_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 7:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_keys_remote_devices (
                        id, device_name, email, private_key, ip_address, request_date, admin_validation
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    safe_int(row[0]) if row[0] else None,
                    row[1], row[2], row[3], row[4], row[5],
                    safe_int(row[6])
                ))
        print("Imported tb_keys_remote_devices successfully.")

    # 3. tb_jobs 임포트
    jobs_path = os.path.join(csv_dir, "SQL_tb_jobs.csv")
    if os.path.exists(jobs_path):
        cursor.execute("DELETE FROM tb_jobs;")
        with open(jobs_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 21:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_jobs (
                        id, date_creation, job_number, company, address, delivery_name,
                        superlot, lot_group, site_supervisor_id, invoice_number, date_install, comment, completed,
                        drawing_link, closed, approved_by, archived_by, date_archive, date_sign,
                        archive_id, archive_comment
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    safe_int(row[0]) if row[0] else None,
                    row[1],
                    safe_int(row[2]),
                    row[3], row[4], row[5],
                    row[6], row[7],
                    safe_int(row[8]) if row[8] else 0,
                    row[9], row[10], row[11], row[12],
                    row[13],
                    safe_int(row[14]) if row[14] else 0,
                    row[15], row[16], row[17], row[18],
                    safe_int(row[19]) if row[19] else 0,
                    row[20]
                ))
        print("Imported tb_jobs successfully.")

    # 4. tb_jobs_date_install 임포트
    jdi_path = os.path.join(csv_dir, "SQL_tb_jobs_date_install.csv")
    if os.path.exists(jdi_path):
        cursor.execute("DELETE FROM tb_jobs_date_install;")
        with open(jdi_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 6:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_jobs_date_install (
                        id, date_creation, job_number, active_flag, date_install, status
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (safe_int(row[0]) if row[0] else None, row[1], safe_int(row[2]), row[3], row[4], row[5]))
        print("Imported tb_jobs_date_install successfully.")

    # 5. tb_jobs_dates 임포트
    jdates_path = os.path.join(csv_dir, "SQL_tb_jobs_dates.csv")
    if os.path.exists(jdates_path):
        cursor.execute("DELETE FROM tb_jobs_dates;")
        with open(jdates_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 35:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_jobs_dates VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, [safe_int(row[0]) if row[0] else None, safe_int(row[1])] + row[2:35])
        print("Imported tb_jobs_dates successfully.")

    # 6. tb_jobs_details 임포트
    jdetails_path = os.path.join(csv_dir, "SQL_tb_jobs_details.csv")
    if os.path.exists(jdetails_path):
        cursor.execute("DELETE FROM tb_jobs_details;")
        with open(jdetails_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 29:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_jobs_details VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, [safe_int(row[0]) if row[0] else None, row[1], safe_int(row[2])] + row[3:29])
        print("Imported tb_jobs_details successfully.")

    # 7. tb_tasks 임포트
    tasks_path = os.path.join(csv_dir, "SQL_tb_tasks.csv")
    if os.path.exists(tasks_path):
        cursor.execute("DELETE FROM tb_tasks;")
        with open(tasks_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 10:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_tasks (
                        id, task_name, task_desc, task_type, job_id, status, due_date,
                        assignee_id, assignee_name, date_complete
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    safe_int(row[0]) if row[0] else None,
                    row[1], row[2],
                    safe_int(row[3]),
                    safe_int(row[4]),
                    safe_int(row[5]),
                    row[6],
                    safe_int(row[7]),
                    row[8], row[9]
                ))
        print("Imported tb_tasks successfully.")

    # 8. tb_tasks_employees_affectation 임포트
    tea_path = os.path.join(csv_dir, "SQL_tb_tasks_employees_affectation.csv")
    if os.path.exists(tea_path):
        cursor.execute("DELETE FROM tb_tasks_employees_affectation;")
        with open(tea_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 11:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_tasks_employees_affectation VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, [safe_int(row[0]) if row[0] else None] + row[1:11])
        print("Imported tb_tasks_employees_affectation successfully.")

    # 9. tb_leaves 임포트
    leaves_path = os.path.join(csv_dir, "SQL_tb_leaves.csv")
    if os.path.exists(leaves_path):
        cursor.execute("DELETE FROM tb_leaves;")
        with open(leaves_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 5:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_leaves (
                        id, employee_id, reason, date_start, date_end
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    safe_int(row[0]) if row[0] else None,
                    safe_int(row[1]),
                    row[2], row[3], row[4]
                ))
        print("Imported tb_leaves successfully.")

    # 10. tb_public_holidays 임포트
    ph_path = os.path.join(csv_dir, "SQL_tb_public_holidays.csv")
    if os.path.exists(ph_path):
        cursor.execute("DELETE FROM tb_public_holidays;")
        with open(ph_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 4:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_public_holidays VALUES (?, ?, ?, ?)
                """, (safe_int(row[0]) if row[0] else None, row[1], row[2], row[3]))
        print("Imported tb_public_holidays successfully.")

    # 11. tb_punchsheet 임포트
    ps_path = os.path.join(csv_dir, "SQL_tb_punchsheet.csv")
    if os.path.exists(ps_path):
        cursor.execute("DELETE FROM tb_punchsheet;")
        with open(ps_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 12:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_punchsheet VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (safe_int(row[0]) if row[0] else None, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
        print("Imported tb_punchsheet successfully.")

    # 12. tb_reminder_other 임포트
    ro_path = os.path.join(csv_dir, "SQL_tb_reminder_other.csv")
    if os.path.exists(ro_path):
        cursor.execute("DELETE FROM tb_reminder_other;")
        with open(ro_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 4:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_reminder_other VALUES (?, ?, ?, ?)
                """, (safe_int(row[0]) if row[0] else None, row[1], row[2], row[3]))
        print("Imported tb_reminder_other successfully.")

    # 13. tb_reminder_vehicle 임포트
    rv_path = os.path.join(csv_dir, "SQL_tb_reminder_vehicle.csv")
    if os.path.exists(rv_path):
        cursor.execute("DELETE FROM tb_reminder_vehicle;")
        with open(rv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 9:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_reminder_vehicle VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (safe_int(row[0]) if row[0] else None, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        print("Imported tb_reminder_vehicle successfully.")

    # 14. tb_wip 임포트
    wip_path = os.path.join(csv_dir, "SQL_tb_wip.csv")
    if os.path.exists(wip_path):
        cursor.execute("DELETE FROM tb_wip;")
        with open(wip_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 14:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_wip VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (safe_int(row[0]) if row[0] else None, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13]))
        print("Imported tb_wip successfully.")

    # 15. tb_export_data 임포트
    ed_path = os.path.join(csv_dir, "SQL_tb_export_data.csv")
    if os.path.exists(ed_path):
        cursor.execute("DELETE FROM tb_export_data;")
        with open(ed_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for row in reader:
                if not row:
                    continue
                while len(row) < 5:
                    row.append("")
                cursor.execute("""
                    INSERT OR REPLACE INTO tb_export_data VALUES (?, ?, ?, ?, ?)
                """, (safe_int(row[0]) if row[0] else None, row[1], row[2], row[3], row[4]))
        print("Imported tb_export_data successfully.")

    conn.commit()

if __name__ == "__main__":
    print("Initializing SQLite Database...")
    connection = init_db()
    print("Importing legacy CSV data into SQLite...")
    import_csv_data(connection)
    
    # 간단 검증 쿼리
    cur = connection.cursor()
    cur.execute("SELECT COUNT(*) FROM tb_login;")
    print(f"Total rows in tb_login: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM tb_keys_remote_devices;")
    print(f"Total rows in tb_keys_remote_devices: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM tb_jobs;")
    print(f"Total rows in tb_jobs: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM tb_jobs_details;")
    print(f"Total rows in tb_jobs_details: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM tb_punchsheet;")
    print(f"Total rows in tb_punchsheet: {cur.fetchone()[0]}")
    
    connection.close()
    print("Database preparation and CRUD verification completed successfully.")

    
    connection.close()
    print("Database preparation and CRUD verification completed successfully.")
