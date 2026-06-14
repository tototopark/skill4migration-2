from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlite3
from src.domain import check_php_bcrypt_compatibility

router = APIRouter(prefix="/auth", tags=["auth"])
DB_FILE = "f:/pe/public_html/test-migration/skill4migration-2/storage/db.sqlite3"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(payload: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    """
    레거시 5.php 기반의 Login API 엔드포인트.
    tb_login 테이블에서 유저를 조회하고 bcrypt 호환성 체크를 수행합니다.
    """
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, login, password, firstname, lastname, right_level, ip_1, ip_2, ip_3, activated FROM tb_login WHERE login = ? AND is_deleted = 0",
        (payload.username,)
    )
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
        
    if not user["activated"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    # PHP bcrypt 비밀번호 검증
    is_valid = check_php_bcrypt_compatibility(payload.password, user["password"])
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return {
        "status": "success",
        "user_id": user["id"],
        "username": user["login"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "right_level": user["right_level"],
        "ips": [user["ip_1"], user["ip_2"], user["ip_3"]]
    }

if __name__ == "__main__":
    print("FastAPI auth.py module syntax check passed.")
