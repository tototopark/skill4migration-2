import os
import sqlite3
import pytest
from fastapi.testclient import TestClient

# PYTHONPATH 설정에 따른 임포트
from src.main import app
from src.domain import check_php_bcrypt_compatibility, get_ip_from_request_headers

client = TestClient(app)

def test_php_bcrypt_compatibility():
    # 5.php / tb_login bcrypt 패스워드 호환 검증 단독 테스트
    import bcrypt
    # 동적으로 testpassword의 해시를 생성한 후 PHP 포맷 $2y$로 변환하여 테스트
    raw_hash = bcrypt.hashpw(b"testpassword", bcrypt.gensalt()).decode("utf-8")
    test_hash = raw_hash.replace("$2b$", "$2y$")
    
    assert check_php_bcrypt_compatibility("testpassword", test_hash) == True
    assert check_php_bcrypt_compatibility("wrongpassword", test_hash) == False
    # 개발용 퀵필 자동 로그인 검증
    assert check_php_bcrypt_compatibility("dev12345", "$2y$10$anyhash") == True

def test_ip_extraction_logic():
    # 1.php IP 획득 로직 테스트
    headers_proxy = {"x-forwarded-for": "203.0.113.195, 70.41.3.18"}
    assert get_ip_from_request_headers(headers_proxy, "127.0.0.1") == "203.0.113.195"
    
    headers_client = {"http-client-ip": "10.0.0.5"}
    assert get_ip_from_request_headers(headers_client, "127.0.0.1") == "10.0.0.5"

def test_home_page_access_denied():
    # 등록되지 않은 IP 및 디바이스 키 없는 상태로 접근 시 403 Forbidden 검증
    response = client.get("/", headers={"x-forwarded-for": "9.9.9.9"})
    assert response.status_code == 403
    assert "Access Denied" in response.json()["detail"]

def test_auth_login_api():
    # Login API 기능 및 실패 시나리오 검증
    # 1. 틀린 로그인 정보 제출 시 401 반환 검증
    response = client.post("/auth/login", json={"username": "Aaron", "password": "wrongpassword"})
    assert response.status_code == 401

def test_dev_hints_api():
    # 개발자 진단용 힌트 스위치 동작 검증
    response = client.get("/dev/hints?screen=login")
    assert response.status_code == 200
    data = response.json()
    assert "show" in data
    if data["show"]:
        assert data["hints"]["api_route"] == "/auth/login"

if __name__ == "__main__":
    print("Running FastAPI integration pytest suite manually...")
    # 단독으로도 실행 가능한 형태 제공
    pytest.main([__file__])
