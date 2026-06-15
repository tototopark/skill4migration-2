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

def test_jobs_api_flow():
    # 1. Create Job via FastAPI POST /jobs/
    import time
    dynamic_job_number = int(time.time()) % 100000
    
    payload = {
        "job_number": dynamic_job_number,
        "company": "FastAPI integration test comp",
        "address": "456 FastAPI St",
        "superlot": "Lot FastAPI",
        "date_creation": "2026-06-15",
        "pages": [
            {"page": "1", "lot": "L1", "member": "Beam X", "gp": True}
        ]
    }
    
    response = client.post("/jobs/", json=payload)
    assert response.status_code == 201
    res_data = response.json()
    assert "id" in res_data
    assert res_data["message"] == "Job created successfully"
    
    # 2. Verify job is listed in GET /jobs/
    list_response = client.get("/jobs/")
    assert list_response.status_code == 200
    jobs = list_response.json()
    assert any(j["job_number"] == dynamic_job_number for j in jobs)
    
    # 3. Update Job via FastAPI PUT /jobs/{job_number}?year=2026
    update_payload = {
        "company": "FastAPI Updated Name",
        "address": "789 FastAPI St",
        "superlot": "Lot FastAPI Rev",
        "date_creation": "2026-06-15",
        "pages": [
            {"page": "1", "lot": "L1", "member": "Beam X - Rev", "gp": True},
            {"page": "2", "lot": "L2", "member": "New Column", "gp": False}
        ]
    }
    update_response = client.put(f"/jobs/{dynamic_job_number}?year=2026", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Job updated successfully"

    # Cleanup the test records from DB so we do not pollute the database
    conn = sqlite3.connect("f:/pe/public_html/test-migration/skill4migration-2/storage/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_jobs WHERE job_number = ? AND strftime('%Y', date_creation) = '2026'", (dynamic_job_number,))
    cursor.execute("DELETE FROM tb_jobs_details WHERE job_number = ? AND strftime('%Y', date_creation) = '2026'", (dynamic_job_number,))
    cursor.execute("DELETE FROM tb_jobs_date_install WHERE job_number = ? AND strftime('%Y', date_creation) = '2026'", (dynamic_job_number,))
    cursor.execute("DELETE FROM tb_wip WHERE job_number = ?", (str(dynamic_job_number),))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Running FastAPI integration pytest suite manually...")
    # 단독으로도 실행 가능한 형태 제공
    pytest.main([__file__])
