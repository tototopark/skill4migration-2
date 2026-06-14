import os
import re
import json

php_dir = "f:/pe/public_html/test-migration/sitepro"
files = [f for f in os.listdir(php_dir) if f.endswith('.php')]

active_files = []
for f in files:
    if "-save" in f.lower() or "save20" in f.lower() or re.search(r'\d{8}', f) or "save_20" in f.lower() or "save-20" in f.lower():
        continue
    if f in ["class.json.php", "comments.tpl.php", "ga.php", "info.php", "polyfill.php"]:
        continue
    active_files.append(f)

analysis_results = []
for fname in sorted(active_files):
    fpath = os.path.join(php_dir, fname)
    if not os.path.isfile(fpath):
        continue
    
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    lines = content.split('\n')
    header_snippet = " | ".join([l.strip() for l in lines[:15] if l.strip()][:4])
    
    # Simple table extractors
    sql_tables = set(re.findall(r'from\s+([a-zA-Z0-9_]+)', content, re.IGNORECASE))
    updates = set(re.findall(r'update\s+([a-zA-Z0-9_]+)', content, re.IGNORECASE))
    inserts = set(re.findall(r'insert\s+into\s+([a-zA-Z0-9_]+)', content, re.IGNORECASE))
    
    tables_used = sql_tables.union(updates).union(inserts)
    # Filter out common false positives
    real_tables = []
    for t in tables_used:
        t_lower = t.lower()
        if t_lower in ["of", "a", "the", "date", "of", "and", "or", "in", "to", "for", "by", "select", "update", "insert", "delete"]:
            continue
        real_tables.append(t)
    
    title_match = re.search(r'<!--(.*?)-->', content, re.DOTALL)
    title_comment = title_match.group(1).strip() if title_match else ""
    if not title_comment:
        # Try to find comment lines inside PHP
        php_comments = re.findall(r'//(.*)', content)
        for c in php_comments[:3]:
            if any(k in c.lower() for k in ["page", "title", "action", "connect", "disconnect", "job", "login", "register"]):
                title_comment = c.strip()
                break
                
    analysis_results.append({
        "file": fname,
        "size": len(content),
        "comment_title": title_comment,
        "snippet": header_snippet[:200],
        "tables": sorted(list(set(real_tables)))
    })

with open("f:/pe/public_html/test-migration/skill4migration-2/scratch/analysis_results.json", "w", encoding="utf-8") as out:
    json.dump(analysis_results, out, indent=2, ensure_ascii=False)

print(f"Analysis saved to scratch/analysis_results.json. Total active files parsed: {len(analysis_results)}")
