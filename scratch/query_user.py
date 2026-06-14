import sqlite3

conn = sqlite3.connect("f:/pe/public_html/test-migration/skill4migration-2/storage/db.sqlite3")
cursor = conn.cursor()
cursor.execute("SELECT id, login, password, right_level FROM tb_login")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
