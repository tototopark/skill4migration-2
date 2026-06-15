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

connections = {}

for fname in sorted(active_files):
    fpath = os.path.join(php_dir, fname)
    if not os.path.isfile(fpath):
        continue
        
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        
    # Find includes / requires
    includes = re.findall(r'(?:include|require)(?:_once)?\s*(?:\(?)\s*[\'"]([a-zA-Z0-9_\-\.\/\\~]+)[\'"]', content, re.IGNORECASE)
    # Find redirects
    redirects = re.findall(r'Location:\s*([a-zA-Z0-9_\-\.\/\\~]+)', content, re.IGNORECASE)
    
    # Check for session_start
    has_session = "session_start" in content
    # Check for ip checks
    has_ip_check = "ip_1" in content or "ip_2" in content or "get_ip" in content
    # Check for role redirects
    has_role_redirect = "right_level" in content or "Role" in content
    # Check for file upload
    has_upload = "move_uploaded_file" in content or "UPLOAD_ERR" in content or "_FILES" in content
    
    # Save results
    connections[fname] = {
        "includes": list(set(includes)),
        "redirects": list(set(redirects)),
        "has_session": has_session,
        "has_ip_check": has_ip_check,
        "has_role_redirect": has_role_redirect,
        "has_upload": has_upload
    }

with open("f:/pe/public_html/test-migration/skill4migration-2/scratch/connections.json", "w", encoding="utf-8") as out:
    json.dump(connections, out, indent=2, ensure_ascii=False)

print("Connections analyzed and saved to scratch/connections.json")
