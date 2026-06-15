import json
import os
import re

# Load inputs
with open("f:/pe/public_html/test-migration/skill4migration-2/scratch/significant_files.json", "r", encoding="utf-8") as f:
    sig_files = json.load(f)
    
with open("f:/pe/public_html/test-migration/skill4migration-2/scratch/connections.json", "r", encoding="utf-8") as f:
    conn_data = json.load(f)

# sitepro directory scan to match family files and devwebsite mirrors
all_files = os.listdir("f:/pe/public_html/test-migration/sitepro")
dev_files = os.listdir("f:/pe/public_html/test-migration/sitepro/devwebsite") if os.path.exists("f:/pe/public_html/test-migration/sitepro/devwebsite") else []

def get_family_and_mirrors(fname):
    base_name, ext = os.path.splitext(fname)
    family = []
    
    # Check for same numbers/names with save prefix or date
    # e.g., 3.php -> 3-save20230322.php
    for f in all_files:
        if f == fname:
            continue
        if f.startswith(base_name + "-save") or f.startswith(base_name + "-Save") or f.startswith(base_name + "_save") or f.startswith(base_name + "-20"):
            family.append(f)
            
    # Check for devwebsite mirror
    has_mirror = fname in dev_files
    mirror_path = f"devwebsite/{fname}" if has_mirror else ""
    
    return family, mirror_path

markdown = """# 수정_09_레거시파일상세분류.md - 레거시 PHP 파일 상세 용도 및 아키텍처 분류 보고서

본 문서는 `sitepro` 레거시 PHP 파일 86개에 대해 진짜 역할, 매핑 카테고리, 파일 간 연결성, 그리고 포팅 시 주의해야 할 엣지 케이스를 정밀 분석하여 마이그레이션 안전성을 확보하기 위한 상세 아키텍처 분류서입니다.

---

## 1. 아키텍처 분류 기준 정의

### 1.1 진짜 역할 (Real Role)
* **화면 표시용 (View)**: HTML/CSS를 에코하거나 화면 템플릿을 로드하는 사용자 화면 페이지.
* **로그인/인증 (Auth)**: 사용자 세션 생성, 비밀번호 검증, IP 및 기기 통제 기능 수행.
* **저장/수정 처리 (Action/Controller)**: 클라이언트의 POST 요청을 수신하여 DB 데이터 삽입/갱신/삭제를 실행하는 API/백엔드 로직.
* **조회 전용 (Query API)**: 단순 데이터를 DB에서 로드하여 JSON, CSV 혹은 특정 형식으로 출력하는 데이터 제공 API.
* **단순 include/library (Library)**: 중복 제거를 위한 유틸리티 함수 그룹 또는 시스템 공통 환경 설정 파일.

### 1.2 매핑 카테고리 (Mapping Category)
* **Wrapper**: 레거시 PHP 주소를 그대로 유지하면서 백엔드의 FastAPI API로 요청을 포워딩/프록시 및 위임하는 껍데기 파일.
* **Boundary**: 파일 시스템 업로드, 외부 이메일(SMTP) 전송, reCAPTCHA 검증 등 외부 환경과의 경계를 담당하는 파일.
* **Mirror**: `devwebsite` 폴더 등에 위치하며 실제 실서비스 코드의 로컬 테스트/백업용 대칭 파일.
* **Library**: 여러 모듈에서 공통 임포트하여 사용하는 내부 종속 모듈.
* **Legacy-only**: 최신 Next.js/FastAPI 스택에는 통합되거나 필요 없어져서 완전히 제거 또는 무시할 예정인 파일.

---

## 2. 레거시 파일별 정밀 아키텍처 매핑

"""

# Classify and append
for r in sig_files:
    fname = r["file"]
    size = r["size"]
    title = r["comment_title"]
    tables = r["tables"]
    
    c = conn_data.get(fname, {
        "includes": [],
        "redirects": [],
        "has_session": False,
        "has_ip_check": False,
        "has_role_redirect": False,
        "has_upload": False
    })
    
    # 1. Determine Real Role
    real_role = "화면 표시용 (View)"
    if fname in ["connect.php", "disconnect.php", "destroysession.php", "register.php"]:
        real_role = "로그인/인증 (Auth)"
    elif "action" in fname.lower() or "update" in fname.lower() or "delete" in fname.lower() or "create" in fname.lower() or title.startswith("UPDATE") or title.startswith("CREATE") or title.startswith("DELETE"):
        real_role = "저장/수정 처리 (Action/Controller)"
    elif "export" in fname.lower() or title.startswith("EXPORT"):
        real_role = "조회 전용 (Query API)"
    elif fname in ["functions.inc.php", "ga.php", "polyfill.php"]:
        real_role = "단순 include/library (Library)"
    elif size < 3000 and len(tables) == 0:
        real_role = "단순 include/library (Library)"
        
    # 2. Determine Mapping Category
    mapping_cat = "Legacy-only"
    if fname in ["index.php", "functions.inc.php"]:
        mapping_cat = "Library"
    elif c["has_upload"] or "export" in fname.lower():
        mapping_cat = "Boundary"
    elif fname in ["1.php", "2.php", "3.php", "4.php", "5.php", "7.php", "9.php", "connect.php", "disconnect.php", "register.php", "PunchSheetAction.php", "create_update_job.php", "update_jobsdetails.php"]:
        mapping_cat = "Boundary / Wrapper 대상"
    elif fname.replace(".php", "") in ["6", "8", "10", "15", "16", "17", "19", "20", "28", "32", "39", "40", "42", "43", "50", "51", "52", "56", "61", "64", "66", "73"]:
        mapping_cat = "Boundary / Wrapper 대상"
    
    # 3. Connections
    family, mirror = get_family_and_mirrors(fname)
    family_str = ", ".join(family) if family else "없음"
    mirror_str = f"[{mirror}](file:///f:/pe/public_html/test-migration/sitepro/{mirror})" if mirror else "없음"
    
    # Common includes detection
    common_includes = []
    if c["includes"]:
        for inc in c["includes"]:
            common_includes.append(inc)
    common_inc_str = ", ".join(common_includes) if common_includes else "없음"
    
    # 4. Edge Cases
    edge_cases = []
    if c["has_ip_check"]:
        edge_cases.append("IP 체크 (ip_1, ip_2, ip_3 검증)")
    if c["has_session"]:
        edge_cases.append("세션 체크 (session_start 및 로그인 존재성)")
    if c["has_role_redirect"] or "right_level" in title.lower():
        edge_cases.append("Role Redirect (right_level 분기)")
    if c["has_upload"]:
        edge_cases.append("파일 업로드 (_FILES 및 move_uploaded_file)")
    if len(tables) > 0:
        edge_cases.append("SQLite 쿼리 호환성 및 Null/Empty 처리")
        
    edge_case_str = " | ".join(edge_cases) if edge_cases else "일반 엣지케이스 없음"
    
    markdown += f"""### 2.{sig_files.index(r)+1} [{fname}](file:///f:/pe/public_html/test-migration/sitepro/{fname})
* **역할/주석 타이틀**: {title if title else '지정되지 않음'}
* **진짜 역할**: **{real_role}**
* **매핑 카테고리**: **{mapping_cat}**
* **연결 관계**:
  * 같은 번호 Family 백업본: `{family_str}`
  * devwebsite 미러 파일: {mirror_str}
  * 임포트한 공통 include 파일: `{common_inc_str}`
* **포팅 시 주의할 엣지케이스**: `{edge_case_str}`

---

"""

with open("f:/pe/public_html/test-migration/skill4migration-2/수정/수정_09_레거시파일상세분류.md", "w", encoding="utf-8") as out:
    out.write(markdown)

print("Detail mapping written successfully to 수정_09_레거시파일상세분류.md")
