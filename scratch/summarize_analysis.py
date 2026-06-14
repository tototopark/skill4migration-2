import json

with open("f:/pe/public_html/test-migration/skill4migration-2/scratch/analysis_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

print(f"{'File':<30} | {'Size':<6} | {'Tables Used':<50} | {'Comment/Title'}")
print("-" * 110)

significant_files = []

for r in results:
    tables = ", ".join(r["tables"])
    # If file contains tables, or has specific keywords in comment or filename
    has_db = len(r["tables"]) > 0
    is_action = any(k in r["file"].lower() for k in ["action", "connect", "session", "disconnect", "register", "update", "functions"])
    is_main_route = r["file"] in ["1.php", "2.php", "3.php", "4.php", "5.php", "index.php"]
    
    if has_db or is_action or is_main_route or r["size"] > 5000:
        significant_files.append(r)
        print(f"{r['file']:<30} | {r['size']:<6} | {tables[:50]:<50} | {r['comment_title']}")

print(f"\nTotal significant files: {len(significant_files)}")

# Save significant files to a separate json
with open("f:/pe/public_html/test-migration/skill4migration-2/scratch/significant_files.json", "w", encoding="utf-8") as out:
    json.dump(significant_files, out, indent=2, ensure_ascii=False)
