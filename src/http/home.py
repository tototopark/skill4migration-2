from fastapi import APIRouter, Depends, HTTPException, Request, status
import sqlite3
from src.domain import get_ip_from_request_headers

router = APIRouter(tags=["home"])
DB_FILE = "f:/pe/public_html/test-migration/skill4migration-2/storage/db.sqlite3"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def enforce_ip_and_device_limit(request: Request, db: sqlite3.Connection = Depends(get_db)):
    """
    레거시 1.php의 IP 접근 통제 및 tb_keys_remote_devices 검증 로직 이식 미들웨어 함수.
    조건 불일치 시 403 Forbidden 예외를 반환합니다.
    """
    client_ip = get_ip_from_request_headers(request.headers, request.client.host if request.client else "127.0.0.1")
    
    # 1. IP 화이트리스트 검증
    cursor = db.cursor()
    cursor.execute(
        "SELECT id FROM tb_login WHERE ip_1 = ? OR ip_2 = ? OR ip_3 = ?",
        (client_ip, client_ip, client_ip)
    )
    ip_match = cursor.fetchone()
    if ip_match:
        return True # IP 일치 시 통과
        
    # 2. IP 불일치 시 Device Validation 검증
    # 쿠키 또는 헤더에서 mydevice (private_key) 추출
    mydevice_key = request.headers.get("x-mydevice-key") or request.cookies.get("mydevice")
    
    if not mydevice_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: Invalid location or unregistered device."
        )
        
    cursor.execute(
        "SELECT id FROM tb_keys_remote_devices WHERE private_key = ? AND admin_validation = 1",
        (mydevice_key,)
    )
    device_match = cursor.fetchone()
    if not device_match:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: Unregistered device key."
        )
    return True

@router.get("/")
def home_index(authorized: bool = Depends(enforce_ip_and_device_limit)):
    """
    1.php 매핑 메인 페이지 API 엔드포인트.
    """
    return {
        "status": "success",
        "message": "Welcome to Pengelly Engineers Dashboard Portal",
        "authorized": authorized
    }

if __name__ == "__main__":
    print("FastAPI home.py module syntax check passed.")
