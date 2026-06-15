import os
import csv

csv_dir = "f:/pe/public_html/test-migration/sitepro/SQL_DL_FILE-Dev"
files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

for fname in sorted(files):
    fpath = os.path.join(csv_dir, fname)
    print(f"=== {fname} ===")
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter='\\')
            for i, row in enumerate(reader):
                if i < 3:
                    print(row)
                else:
                    break
    except Exception as e:
        print("Error:", e)
