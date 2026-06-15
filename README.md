# Sitepro Legacy Migration Project (FastAPI + SQLite)

본 프로젝트는 레거시 PHP 기반의 Jumbo Drawing & Jobs 관리 시스템인 `sitepro` 서비스를 현대적인 **FastAPI(Python) + SQLite** 백엔드 아키텍처로 기능적 유실 없이 이식하는 포트폴리오 프로젝트입니다.

---

## 1. 프로젝트 개요

* **레거시 스택**: PHP (MySQL 의존성, 317개 난독화/백업 파일 혼재)
* **신규 마이그레이션 스택**: Python (FastAPI + SQLite + Pytest)
* **주요 목표**:
  * 비즈니스 로직, 접근 보안 및 구형 bcrypt 암호화 체계의 100% 호환성 확보.
  * API 개별 파일 저장 및 300줄 이하 모듈화 규칙 준수.
  * 데이터 CRUD 처리를 위한 독립 실행형 파이프라인 구축.
  * 이중 게이트(Gate 1 & Gate 2) 정밀 분석 및 대조 회귀 검증.

---

## 2. 작업 수행 이력 및 산출물 (수정 이력)

모든 분석 계획 및 마이그레이션 이력은 사용자의 전용 규칙에 따라 `수정/` 디렉토리에 순차적으로 정리되어 있습니다.

* **[수정_07_레거시전수분석.md](수정/수정_07_레거시전수분석.md)**: 317개 PHP 파일 중 실제 동작하는 86개 활성 후보 선별 및 15개 관계형 DB 테이블 1:1 의존성 매핑 분석 보고서.
* **[수정_09_레거시파일상세분류.md](수정/수정_09_레거시파일상세분류.md)**: 활성 파일별 진짜 역할(View/Auth/Action/Query/Library), 맵핑 카테고리(Wrapper/Boundary/Mirror/Legacy-only) 및 주의할 엣지 케이스 상세 명세서.
* **[수정_10_마이그레이션구현계획.md](수정/수정_10_마이그레이션구현계획.md)**: 연동 중요도에 따른 우선순위 그룹화 및 파일 분할 구현 계획서.
* **[수정_11_작업이식완료_walkthrough.md](수정/수정_11_작업이식완료_walkthrough.md)**: Group 1 핵심 작업(Jobs) CRUD API/파이프라인 이식 성공 및 pytest 회귀 대조 통과 보고서.

---

## 3. 핵심 마이그레이션 기술 요약

* **PHP Bcrypt 호환성 교정**: PHP의 구형 해시 포맷 `$2y$`를 파이썬 표준인 `$2b$` 포맷으로 실시간 교환 검증 처리.
* **독립 실행형 파이프라인 TDD**: 각 파이프라인 파일(`src/service/*_pipeline.py`) 하단에 `if __name__ == "__main__"` 테스트 블록을 내장하여, 웹 서버 없이도 단독 실행을 통한 데이터 CRUD 무결성 assert 검사 수행.
* **통합 테스트 클린업**: 테스트 단계에서 발생한 데이터들이 실제 데이터베이스에 오염(Pollution)을 남기지 않도록, 검증 직후 테스트 레코드를 데이터베이스에서 자동으로 롤백 및 삭제(Clean-up)하도록 설계.

---

## 4. 실행 및 테스트 방법

### 4.1 SQLite 데이터 적재
```bash
python src/repository.py
```

### 4.2 백엔드 파이프라인 단독 CRUD 테스트
```bash
python -m src.service.jobs_pipeline
```

### 4.3 통합 API 회귀 테스트 스위트 구동
```bash
python -m pytest
```
