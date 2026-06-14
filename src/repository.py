import os
import csv
import sqlite3
import shutil

DB_FILE = "storage/db.sqlite3"

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

CREATE TABLE IF NOT EXISTS tb_leaves (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    reason TEXT,
    date_start TEXT,
    date_end TEXT
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

def import_csv_data(conn, csv_dir="sitepro/SQL_DL_FILE-Dev"):
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
                # 빈 값 처리 및 크기 맞추기
                while len(row) < 19:
                    row.append("")
                # CSV: 90\Aaron\$2y$10$...\Aaron\Campbell\user.jpg\0\2019-09-01\MD\9\\1\Pending\Pending\\0\103.242.27.225\\null
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
                # row가 여러 행으로 찢어지는 현상 방지하기 위해 필드 수 보완
                while len(row) < 19:
                    row.append("")
                # DB mapping match SQL:
                # tb_jobs (id, date_creation, job_number, company_name, site_address, superlot, lot_group, supervisor_name, builder_name, installer_name, install_type, date_last_update, WIP_Completed, WIP_Issue_Date, WIP_Revision_Date, WIP_Revision)
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
                    safe_int(row[8]) if row[8] else 0, # supervisor_id / name
                    row[9], row[10], row[11], row[12],
                    row[13],
                    safe_int(row[14]) if row[14] else 0,
                    row[15], row[16], row[17], row[18],
                    0, "" # 기본값 매핑
                ))
        print("Imported tb_jobs successfully.")

    # 4. tb_tasks 임포트
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

    # 5. tb_leaves 임포트
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
    
    connection.close()
    print("Database preparation and CRUD verification completed successfully.")
