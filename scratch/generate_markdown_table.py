import json

with open("f:/pe/public_html/test-migration/skill4migration-2/scratch/significant_files.json", "r", encoding="utf-8") as f:
    files = json.load(f)

# Group files by logical components
# 1. Auth & Session: Login, Register, Connect, Disconnect, destroysession
# 2. Main Routers & Pages: 1.php ~ 5.php, index.php
# 3. Actions / APIs: update_*.php, PunchSheetAction.php, create_update_job.php
# 4. Other numeric files (6.php ~ 73.php) - categorize them by comment title

auth_session = []
main_pages = []
actions = []
others = []

for r in files:
    fname = r["file"]
    title = r["comment_title"]
    tables = ", ".join(r["tables"])
    
    # Simple classification
    if fname in ["connect.php", "disconnect.php", "destroysession.php", "register.php"]:
        auth_session.append(r)
    elif fname in ["index.php", "functions.inc.php"]:
        main_pages.append(r)
    elif fname.endswith(".php") and ("update" in fname or "action" in fname.lower() or fname.startswith("PunchSheetAction")):
        actions.append(r)
    elif fname in ["1.php", "2.php", "3.php", "4.php", "5.php"]:
        main_pages.append(r)
    else:
        others.append(r)

def format_table(group_list):
    out = "| 파일명 | 크기 (Bytes) | 주요 테이블 | 역할/주석 타이틀 |\n"
    out += "|---|---|---|---|\n"
    for r in group_list:
        title = r["comment_title"].replace("\n", " ").replace("\r", "")
        tables = ", ".join(r["tables"])
        out += f"| [{r['file']}](file:///f:/pe/public_html/test-migration/sitepro/{r['file']}) | {r['size']:,} | {tables} | {title} |\n"
    return out

markdown = "# 레거시 PHP 파일 전수 분석 보고서 (1:1 매핑)\n\n"
markdown += "## 1. 인증 및 세션 관련 파일\n\n"
markdown += format_table(auth_session) + "\n"

markdown += "## 2. 메인 페이지 및 라우팅 허브\n\n"
markdown += format_table(main_pages) + "\n"

markdown += "## 3. 주요 비즈니스 액션 및 API 처리 파일\n\n"
markdown += format_table(actions) + "\n"

markdown += "## 4. 개별 기능별 숫자 파일 (1.php ~ 73.php)\n\n"
markdown += format_table(others) + "\n"

with open("f:/pe/public_html/test-migration/skill4migration-2/scratch/table.md", "w", encoding="utf-8") as out:
    out.write(markdown)

print("Markdown table generated at scratch/table.md")
