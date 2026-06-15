import re

with open("f:/pe/public_html/test-migration/skill4migration-2/수정/수정_09_레거시파일상세분류.md", "r", encoding="utf-8") as f:
    content = f.read()

# Legacy-only 로 분류된 항목들을 식별하여 세부 이유를 주입
# 예시 치환:
# * **매핑 카테고리**: **Legacy-only**
# -> * **매핑 카테고리**: **Legacy-only** (이유: ...)

# We will define mappings of legacy-only reasons based on file name or type
reasons = {
    "11.php": "단순 페이지 레이아웃 가이드 및 임시 화면으로 신규 React 구조에서는 필요 없음",
    "13.php": "FastAPI 사용자 제어 라우터(`DELETE /api/users/{id}`) API로 통합 대체 예정",
    "14.php": "FastAPI 사용자 비밀번호 리셋 라우터(`POST /api/users/{id}/reset-password`) API로 통합 대체 예정",
    "18.php": "FastAPI 본인 비밀번호 변경 API 및 React 회원 정보 페이지 내 입력 기능으로 흡수 통합 예정",
    "21.php": "차량 알림 정보 수정 API (`PUT /api/reminders/vehicles/{id}`)로 통합 대체 예정",
    "22.php": "차량 알림 삭제 API (`DELETE /api/reminders/vehicles/{id}`)로 통합 대체 예정",
    "23.php": "차량 알림 생성 API (`POST /api/reminders/vehicles`)로 통합 대체 예정",
    "24.php": "안전 교육 날짜 업데이트 API (`PUT /api/reminders/sitesafe/{id}`)로 통합 대체 예정",
    "25.php": "기타 자격증 알림 수정 API (`PUT /api/reminders/other/{id}`)로 통합 대체 예정",
    "26.php": "기타 자격증 알림 삭제 API (`DELETE /api/reminders/other/{id}`)로 통합 대체 예정",
    "27.php": "기타 자격증 알림 생성 API (`POST /api/reminders/other`)로 통합 대체 예정",
    "29.php": "FastAPI 작업자 일감 삭제 API (`DELETE /api/tasks/{id}`)로 통합 대체 예정",
    "2bis.php": "화이트보드 메인 화면 로직으로, 신규 FastAPI 화이트보드 쿼리 API (`GET /api/whiteboard`)로 흡수 통합 예정",
    "30.php": "작업자 일감 생성 API (`POST /api/tasks`)로 통합 대체 예정",
    "31.php": "작업자 일감 진행율 업데이트 API (`PUT /api/tasks/{id}/progress`)로 통합 대체 예정",
    "33.php": "펀치시트 개별 액션 API (`POST /api/punchsheets/{id}/actions`)로 통합 대체 예정",
    "34.php": "단순 시스템 동작 진단용 임시 파일로 포팅 대상에서 영구 제외",
    "35.php": "기기 관리 API (`PUT /api/devices/{id}`)로 통합 대체 예정",
    "36.php": "기기 등록 승인 API (`POST /api/devices`)로 통합 대체 예정",
    "37.php": "기기 삭제 API (`DELETE /api/devices/{id}`)로 통합 대체 예정",
    "3bis.php": "레거시 빌더가 생성한 임시 뷰 페이지로 신규 작업 상세 API 및 리스트 통합 시 삭제 처리",
    "41.php": "WIP 검수 완료 처리 API (`POST /api/wip/{id}/complete`) 및 상태 토글로 흡수",
    "44.php": "공휴일 수정 API (`PUT /api/holidays/{id}`)로 통합 대체 예정",
    "45.php": "연차 상태 승인/수정 API (`PUT /api/leaves/{id}`)로 통합 대체 예정",
    "46.php": "공휴일 등록 API (`POST /api/holidays`)로 통합 대체 예정",
    "47.php": "연차 신청 등록 API (`POST /api/leaves`)로 통합 대체 예정",
    "48.php": "공휴일 삭제 API (`DELETE /api/holidays/{id}`)로 통합 대체 예정",
    "49.php": "연차 신청 삭제 API (`DELETE /api/leaves/{id}`)로 통합 대체 예정",
    "4bis.php": "펀치시트 통계/정보 조회 API 및 React 컴포넌트로 흡수 통합 예정",
    "4bisSHOP.php": "공장 관점의 펀치시트 조회 API 및 전용 뷰 탭으로 흡수 통합 예정",
    "53.php": "데이터 백업 내보내기 준비 API (`POST /api/export/prepare`)로 통합 대체 예정",
    "54.php": "데이터 JSON/CSV 파일 추출 API (`GET /api/export/download`)로 통합 대체 예정",
    "55.php": "어드민 전용 데이터 강제 백업 수동 실행 API로 통합 및 배치 스크립트로 이관 예정",
    "57.php": "생산 계획 수정 API (`PUT /api/production/{id}`)로 통합 대체 예정",
    "58.php": "생산 계획 등록 API (`POST /api/production`)로 통합 대체 예정",
    "59.php": "생산 계획 삭제 API (`DELETE /api/production/{id}`)로 통합 대체 예정",
    "60.php": "화이트보드 메모(Week Notes) 업데이트 API (`PUT /api/whiteboard/notes/{id}`)로 통합 대체 예정",
    "62.php": "도색 작업 완료 여부 토글 API (`POST /api/jobs/{id}/painting/toggle`)로 통합 대체 예정",
    "63.php": "도색 작업 코멘트 업데이트 API (`PUT /api/jobs/{id}/painting/comment`)로 통합 대체 예정",
    "65.php": "파스너 부품 재고 저장 API (`POST /api/fasteners`)로 통합 대체 예정",
    "69.php": "물리 사진 회전 로직으로 FastAPI 미디어 제어 API (`POST /api/media/{id}/rotate`)로 통합 대체 예정",
    "70.php": "개발자 전용 사진 회전 진단용 파일로 포팅 대상에서 영구 제외",
    "71.php": "레거시 빌더 보조 통계용 임시 파일로 포팅 대상에서 영구 제외",
    "72.php": "디바이스 접속 진단용 보조 임시 파일로 포팅 대상에서 영구 제외",
    "disconnect.php": "FastAPI 인증 로그아웃 API (`POST /api/auth/logout`)로 통합 대체 예정",
    "destroysession.php": "FastAPI 세션 파괴 및 토큰 만료 처리 로직으로 통합 대체 예정"
}

# Apply replacements
for fname, reason in reasons.items():
    # Find block starting with ### 2.X [fname] or similar
    # e.g., ### 2.1 [1.php](...)
    pattern = rf"(### 2\.\d+ \[{fname}\]\(.*?file:\/\/.*?\)\n\* \*\*역할/주석 타이틀\*\*: .*?\n\* \*\*진짜 역할\*\*: .*?\n\* \*\*매핑 카테고리\*\*: \*\*Legacy-only\*\*)"
    replacement = r"\1" + f" (이유: {reason})"
    content = re.sub(pattern, replacement, content)

with open("f:/pe/public_html/test-migration/skill4migration-2/수정/수정_09_레거시파일상세분류.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Legacy-only reasons added to 수정_09_레거시파일상세분류.md")
