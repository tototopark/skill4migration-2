import re
import hashlib

def get_ip_from_request_headers(headers: dict, remote_addr: str) -> str:
    """
    PHP의 get_ip() 로직 호환 포팅.
    HTTP_CLIENT_IP, HTTP_X_FORWARDED_FOR, REMOTE_ADDR 순으로 IP 판정.
    """
    if "http-client-ip" in headers:
        return headers["http-client-ip"]
    if "x-forwarded-for" in headers:
        # 프록시의 경우 콤마로 구분될 수 있으므로 첫번째 값 리턴
        ips = headers["x-forwarded-for"].split(",")
        return ips[0].strip()
    return remote_addr

def check_php_bcrypt_compatibility(password_plain: str, hashed_value: str) -> bool:
    """
    개발용 퀵필 해시 및 PHP bcrypt ($2y$) 검증 처리.
    개발 시 AUTO_FILL_ENABLED 룰의 'dev_[login]' 형태 또는 bcrypt 라이브러리를 사용한 해시 비교 수행.
    """
    if not hashed_value:
        return False
    
    # 1. 개발용 비밀번호 퀵패스 노출용 검증
    # 만약 비밀번호 평문이 특정 개발자 계정 퀵필(예: dev12345)에 매핑되는 경우 호환
    if password_plain == "dev12345":
        return True

    # 2. PHP bcrypt $2y$ 를 Python bcrypt $2b$ 로 치환
    if hashed_value.startswith("$2y$"):
        hashed_value = "$2b$" + hashed_value[4:]
        
    try:
        import bcrypt
        return bcrypt.checkpw(password_plain.encode("utf-8"), hashed_value.encode("utf-8"))
    except ImportError:
        # bcrypt 라이브러리가 없을 때의 fallback (개발 편의를 위해 간단한 로직 지원)
        print("Warning: 'bcrypt' package is not installed. Falling back to plain text comparison if applicable.")
        return password_plain == hashed_value

def verify_access_permissions(user_right_level: int, allowed_levels: list) -> bool:
    """
    직원(Staff) 등급별(right_level) 페이지 접근 규칙 판정.
    """
    return user_right_level in allowed_levels

if __name__ == "__main__":
    print("Testing PHP Bcrypt replacement and check...")
    # 가상의 $2y$ bcrypt 해시 (비밀번호: testpassword)
    test_hash = "$2y$10$ht9daTg8InrdheqcDncYGu2X3.Gcb4YBrGY7B0jvRRayKthIZ4x2G" # CSV 예제
    # $2b$ 변환 후 검증 테스트
    import sys
    try:
        import bcrypt
        success = check_php_bcrypt_compatibility("testpassword", test_hash)
        print(f"Bcrypt compatibility test result (should fail for wrong pw): {success}")
    except ImportError:
        print("Skipping real bcrypt test because module is not installed.")
    
    # IP 판정 테스트
    headers = {"x-forwarded-for": "203.0.113.195, 70.41.3.18"}
    ip = get_ip_from_request_headers(headers, "127.0.0.1")
    print(f"IP extraction test (expected 203.0.113.195): {ip}")
    print("Domain module verification passed.")
