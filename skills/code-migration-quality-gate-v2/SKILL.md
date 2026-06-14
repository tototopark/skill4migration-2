---
name: code-migration-quality-gate-v2
description: Use when migrating legacy projects, rewriting codebases, porting applications (e.g. PHP to React/Next.js/FastAPI), or mapping old menus/functions to a new tech stack. Ensures zero functional omissions and absolute fidelity. Focuses on completing DB loader setup and authentication domain porting without stopping to ask questions. Always use this skill for codebase migration tasks. Do not use for writing new standalone apps from scratch or non-technical project management.
---

# Code Migration Quality Gate v2 — 무개입 단독 기동 마이그레이션 스킬

이 스킬은 레거시 코드베이스에서 신규 기술 스택으로 시스템을 이전 및 포팅할 때, AI 에이전트가 사용자에게 질문하며 작업을 중단하지 않고 1단계(SQLite 스키마 및 CSV 로더 작성)와 2단계(bcrypt 호환 및 IP/디바이스 보안 검증)를 단독 실행형 테스트를 통해 한 번에 자동 완결하도록 제어하는 **Process + Rigid** 규율 스킬입니다.

## Goal
레거시 소스 코드가 가진 데이터 스키마와 인증/보안 규칙을 단 하나의 기능 누락도 없이 보존하여 마이그레이션하며, TDD 기반의 단독 기동 스크립트 실행으로 100% 무결성을 스스로 입증합니다.

## Foundational Principle
**Violating the letter of the rules is violating the spirit of the rules.**

---

## Iron Laws

### 1. No-Interruption Self-Completion (무질문 원스톱 완결)
**작업 중 사용자에게 진행 방식을 묻거나 질문하여 멈추지 말라.**
- 마이그레이션 착수 시, 레거시 파일과 DB CSV 파일 구조를 독립적으로 전수분석하여 `repository.py`와 `domain.py`를 즉시 스스로 작성하고 자체 테스트까지 한 번에 완료해야 한다.
- 에러나 타입 불일치가 나면 멈추어 묻지 말고, SQLite DDL과 파이썬 캐스팅 필터 예외 처리를 디버깅하며 스스로 해결하라.

### 2. Standalone Executable TDD (독립 기동 검증 필수)
**모든 백엔드 모듈은 uvicorn/웹 서버 없이 단독 실행하여 데이터 무결성을 입증해야 한다.**
- `if __name__ == "__main__"` 테스트 기동 블록을 파일 하단에 필히 구현하고, 데이터베이스 레코드 수 검증 쿼리 및 해시 검증 결과를 터미널 상에 직관적으로 출력되게 하라.

### 3. PHP Bcrypt `$2y$` Replacement (Bcrypt 강제 치환 및 호환성)
**PHP 고유의 `$2y$` 시작 bcrypt 해시는 파이썬 검증 라이브러리 연동 전 반드시 `$2b$`로 변환하여 로직 상에 안착시켜라.**
- 개발 환경의 원활한 TDD 생산성을 지원하기 위해 `dev_[login]` 및 `dev12345` 등의 개발자용 퀵필 자동입력 검증 우회 규칙을 함께 유지하라.

### 4. Zero-Assumption Schema Preservation (스키마 100% 보존)
**CSV 헤더의 컬럼 수와 데이터 정합성을 자의적으로 생략하거나 무시하지 말라.**
- 데이터 이식 실패의 핵심 원인이 되는 타입 미스매치(`integer` vs `date` 문자열 등)를 방어하도록 `safe_int` 및 null 방어 코드를 적용해 스키마 격차를 완전히 제거하라.

---

## Rationalization Patterns to Reject

| 합리화 | 차단 |
|---|---|
| "스키마에 누락된 컬럼이 사소해서 질문으로 물어보려 했다" | **질문하지 말고 레거시 PHP 소스 코드를 교차 검증하여 컬럼 목적을 추정 매핑하라.** |
| "데이터 타입 에러가 나서 마이그레이션을 일시 중지하겠다" | **중지하지 말고 모든 필드에 빈 값 및 캐스팅 예외 처리를 추가하여 로더의 견고함을 극대화하라.** |
| "bcrypt 패키지가 없어 해시 검증 단독 테스트를 생략하겠다" | **패키지가 없으면 fallback 구문을 적용하고 테스트 출력을 통해 우회 동작을 스스로 보증하라.** |

---

## Verification Checklist
- [ ] **1단계: 단독 로더 검증**: `python src/repository.py` 실행 시 오류 없이 legacy 데이터 로드가 완료되고, Record Count 쿼리가 출력되는가?
- [ ] **2단계: 도메인 룰 검증**: `python src/domain.py` 실행 시 PHP bcrypt 변환 테스트 및 IP 추출 기능이 정상 작동(True/False 검증)하는가?
- [ ] **사용자 룰 반영**: 변경된 산출물들이 `수정` 폴더 및 `skill4migration-2` 하위에 엄격히 배치되어 관리되는가?
- [ ] **빌드 및 린트 에러 0개**: 문법 오류나 가져오기(import) 오류가 없는가?
