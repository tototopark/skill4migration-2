import os
from fastapi import APIRouter

router = APIRouter(prefix="/dev", tags=["dev"])

# 전역 Config 스위치 옵션 (기본값 False)
SHOW_DEV_HINTS = os.getenv("SHOW_DEV_HINTS", "true").lower() == "true"
AUTO_FILL_ENABLED = os.getenv("AUTO_FILL_ENABLED", "true").lower() == "true"

@router.get("/hints")
def get_dev_hints(screen: str = "home"):
    """
    Iron Law 6 규정: 환경 변수 스위치 상태에 따라 진단용 힌트(DevHints) 제공.
    비활성화 시 Render None 효과를 위해 빈 데이터를 반환하도록 처리합니다.
    """
    if not SHOW_DEV_HINTS:
        return {"show": False, "hints": {}}

    # 화면 정보에 따른 API 라우트 경로, 컴포넌트 파일 경로, 참조 DB 테이블 매핑
    hints_database = {
        "home": {
            "api_route": "/",
            "frontend_file": "f:/pe/public_html/test-migration/skill4migration-2/src/http/home.py",
            "db_tables": ["tb_login", "tb_keys_remote_devices"],
            "business_rules": "IP address filter & remote device key validation"
        },
        "login": {
            "api_route": "/auth/login",
            "frontend_file": "f:/pe/public_html/test-migration/skill4migration-2/src/http/auth.py",
            "db_tables": ["tb_login"],
            "business_rules": "PHP Bcrypt $2y$ compatibility validation. Quick fill: dev12345"
        },
        "jobs": {
            "api_route": "/jobs",
            "frontend_file": "f:/pe/public_html/test-migration/skill4migration-2/src/http/jobs.py",
            "db_tables": ["tb_jobs"],
            "business_rules": "Job state query & supervisor association"
        }
    }

    selected_hint = hints_database.get(screen, hints_database["home"])
    
    return {
        "show": True,
        "auto_fill_enabled": AUTO_FILL_ENABLED,
        "hints": selected_hint
    }

if __name__ == "__main__":
    print("Dev hints config: SHOW_DEV_HINTS =", SHOW_DEV_HINTS)
    print("Dev hints config: AUTO_FILL_ENABLED =", AUTO_FILL_ENABLED)
    print("FastAPI dev_hints.py module syntax check passed.")
