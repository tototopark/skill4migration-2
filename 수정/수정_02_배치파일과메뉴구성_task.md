# Task List - sitepro 마이그레이션

- [x] **1단계: SQLite 스키마 설계 및 데이터 로더 작성**
  - [x] `SQL_DL_FILE-Dev` 폴더 내의 CSV 파일들을 분석하여 SQLite 테이블 정의 (`tb_login`, `tb_jobs`, `tb_keys_remote_devices` 등)
  - [x] CSV 데이터를 SQLite DB로 로딩하는 standalone script 작성 (`src/repository.py`)
  - [x] `if __name__ == "__main__"` 테스트 기동 블록을 통해 CRUD 기본 동작 무결성 확인
- [x] **2단계: 공통 비즈니스 로직 및 bcrypt 호환 처리 구현**
  - [x] `functions.inc.php` 및 `1.php`에 정의된 핵심 룰 이전 (`src/domain.py`, `src/service.py`)
  - [x] PHP `$2y$` 시작 bcrypt 패스워드 호환 검증기 구현
  - [x] IP 및 디바이스(private key) 검증 로직 구현
- [ ] **3단계: API 엔드포인트 구현 (FastAPI)**
  - [ ] `auth.py`, `jobs.py`, `home.py` 개별 모듈화 설계 (파일당 300줄 제약 엄수)
  - [ ] 메인 라우터 `api_router.py` 연결
- [ ] **4단계: 개발자 진단용 힌트(DevHints) 및 스위치 추가**
  - [ ] 화면 하단에 바인딩할 API, 파일 경로 메타데이터 수집 컴포넌트 설계
  - [ ] 환경 변수 (`SHOW_DEV_HINTS`) 연동 스위치 개발
- [ ] **5단계: Gate 2 회귀 대조 검증**
  - [ ] `1.php`, `5.php`와 구현된 API 1:1 대조 및 권한별 접근 제어 테스트
