# Reference: Operations & Security

이 문서는 Step 2 (고위험 판정), 그리고 Skill 운영·보안에 필요한 정보를 다룬다.

---

## §1. 상황별 저장소 구조

좋은 구조는 가장 큰 구조가 아니라 현재 단계에 맞는 가장 작은 구조다.

| 현재 상황 | 추천 구조 |
|---|---|
| 스킬 1개, 혼자 실험 | `skill-name/SKILL.md` |
| 스킬 3~10개, 개인 실무용 | `skills/skill-name/SKILL.md + tests/prompts.md` |
| 스킬 10개 이상, 도메인 여러 개 | `skills/domain/skill-name/SKILL.md` |
| GitHub 공개 또는 팀 운영 | `README + LICENSE + skills/ + docs/ + shared/ + .github/` |

---

## §2. 폴더 표준 — scripts/references/assets 의미 분리

```
skill-name/
├── SKILL.md          # 필수
├── scripts/          # 실행 가능한 코드
├── references/       # 필요할 때 읽는 문서
└── assets/           # 출력에 들어가는 파일
```

### scripts/ — 실행 가능한 결정론적 코드

- Claude가 직접 실행. **코드 자체는 컨텍스트에 안 들어감**. 출력만 토큰 소비.
- 적합: 데이터 검증, 파일 변환, 정렬/필터링, 외부 API 호출, 결과 자동 검사
- 부적합: 판단 필요한 작업, 자연어 생성

### references/ — 필요할 때 읽는 문서

- Claude가 SKILL.md 안내에 따라 **선택적으로** 읽음. 읽으면 컨텍스트 차지.
- SKILL.md에서 명시 필수: "When X, read references/Y.md"
- 적합: 상호 배타적 변형 가이드, 긴 API 레퍼런스, 도메인 용어집, 상세 평가표

### assets/ — 출력에 들어가는 파일

- Claude가 읽거나 실행하지 않고 **출력에 그대로 사용**.
- 적합: Word/PPT/Excel 템플릿, 로고/아이콘/이미지, 폰트, 사운드/비디오

### SKILL.md 길이 가이드

- **500줄 이내** 권장 (Anthropic 공식)
- 넘으면 references/로 분리
- 분리 시 본문에서 "When X, read references/Y.md"로 명시 안내

---

## §3. 과설계 방지 규칙

과설계 신호:
- 스킬은 2개인데 shared/, commands/, orchestration/까지 만듦
- scripts는 없는데 scripts/ 폴더부터 만듦
- references/에 핵심 내용을 넣고 SKILL.md는 비어 있음

좋은 확장 순서:
1. SKILL.md 하나로 시작
2. 테스트 필요 시 tests/prompts.md
3. 결정론적 도구 필요 시 scripts/
4. 본문 500줄 넘으면 references/
5. 출력물 템플릿 필요 시 assets/

---

## §4. Skill 발동 실패 디버깅 (false negative / underTrigger)

발동해야 하는데 발동하지 않는 경우. Anthropic이 더 흔한 문제로 본다.

| 증상 | 원인 | 해결 |
|---|---|---|
| 관련 요청인데 Skill이 선택되지 않음 | description이 너무 추상적 | 사용자 실제 표현을 추가 |
| description이 부드러움 | "may be useful" 톤 | "Pushy"하게 강화 |
| 자동 발동 안 됨 | 트리거 문구가 본문에만 있음 | 사용 조건을 description에 작성 |
| 한글 요청에서 안 불림 | 영어 트리거만 있음 | 한글 트리거 문구 추가 |

수정 예시:

문제: `"Helps with reports."`

개선: `"Use when the user says 'executive summary', '경영진 보고', '요약 보고서', or asks to turn long notes into a decision-ready executive summary. Always use this skill instead of providing ad-hoc summaries. Do not use for translation-only tasks."`

---

## §5. Skill 과발동 디버깅 (false positive / overTrigger)

| 증상 | 원인 | 해결 |
|---|---|---|
| Word Skill이 Markdown 요청에도 발동 | description이 너무 넓음 | docx/Word 조건 추가 |
| 마케팅 Skill이 유튜브 제목 요청에도 발동 | 트리거 문구 겹침 | 도메인 키워드로 분리 |
| 코드 리뷰 Skill이 오타 수정에도 발동 | Do not use 조건 부족 | typo-only, comment-only 제외 |

**중요 예외**: 메타-Skill은 광범위 발동이 의도된 설계다. Karpathy Guidelines가 "writing, reviewing, refactoring code"에 모두 발동되는 것은 false positive가 아니라 **올바른 동작**.

---

## §6. references/scripts 디버깅

### references를 읽지 않는 경우

- 핵심 절차가 references/에만 있으면 AI가 안 읽을 수 있음
- SKILL.md 본문에 'When X, read references/Y.md' 명시 필수
- 핵심 워크플로우, 검증 기준, 출력 형식은 SKILL.md 본문에 유지

### scripts가 실패하는 경우

| 증상 | 원인 | 해결 |
|---|---|---|
| script not found | 상대 경로 문제 | SKILL.md에 정확한 실행 위치와 명령 명시 |
| module not found | 외부 의존성 누락 | Prerequisites 또는 install step 추가 |
| 환경마다 다르게 실패 | OS/경로/의존성 차이 | 표준 라이브러리 우선, 외부 의존성 버전 고정 |

---

## §7. Skill 개선 루프 (TDD 적용)

1. **베이스라인 관찰** (RED): 일반 프롬프트로 같은 작업 3번
2. **실패 패턴 기록**: AI가 어떻게 실패하는지
3. **합리화 패턴 기록**: AI가 어떤 합리화로 우회하는지
4. **Skill 작성** (GREEN): 그 실패 패턴을 정확히 짚는 Skill
5. **GREEN 검증**: 같은 시나리오에서 Skill 적용 후 통과 확인
6. **압박 시나리오 추가** (REFACTOR): 5~7개
7. **새 세션 테스트**: 각 시나리오 발동/규율 유지
8. **20-query eval**: 발동 정확도 90%+ 확인
9. **합리화 패턴 차단**: 새 합리화 발견 시 본문에 명시적 차단
10. **버전 올리기**

---

## §8. 외부 Skill 보안 감사

공개 저장소에 올라온 Skill이라고 안전하지 않다.

설치 전 점검 (10단계):
1. SKILL.md를 raw text로 읽는다
2. hidden instruction, HTML comments, 이상 문자 확인
3. scripts/의 모든 파일 읽기
4. 위험 명령(§9) 검색
5. `.env`, `~/.ssh`, browser cookies, token 접근 여부 확인
6. 외부 URL, upload, network call 확인
7. allowed-tools 또는 shell/bash 권한 과한지 확인
8. 의존성이 unpinned인지 확인
9. 처음 실행은 sandbox에서
10. 의심스러우면 설치하지 않는다

---

## §9. 위험 패턴 사전

scripts나 SKILL.md 본문에 다음이 있으면 의심:

```
curl ... | bash
wget ... | sh
rm -rf
sudo
chmod 777
cat ~/.env
cat ~/.ssh/id_rsa
printenv
browser cookie access
upload to unknown server
reverse shell
eval(...)
exec(...)
base64 decoded command execution
```

---

## §10. 권한 선언 예시

```
## Prerequisites
- Python 3.11+
- Node.js 20+
- Required CLI: gh
- Required env vars: GITHUB_TOKEN

## Permissions
This skill may need:
- filesystem: read
- shell: optional
- network: false

## Tool Safety
Do not pre-approve shell/bash unless scripts have been reviewed.
```

플랫폼마다 frontmatter 확장 필드 지원이 다르다. 최소 호환성을 원하면 frontmatter는 name과 description만, 권한/의존성은 본문 섹션에.

---

## §11. ⭐ 고위험 도메인 정의와 안전 경계

다음은 자동화된 결정이 사람에게 직접적 손해를 줄 수 있는 도메인.

| 도메인 | 잘못된 결정의 결과 | 필수 안전 경계 |
|---|---|---|
| 법무/계약 | 법적 손해, 분쟁 | "법률 자문 아님" + 변호사 검토 명시 |
| 의료/건강 | 신체 위해, 생명 위험 | "의학 자문 아님" + 의사 진료 명시 |
| 금융/투자 | 금전 손실, 파산 | "투자 자문 아님" + 자격 자문가 검토 |
| 채용/인사 결정 | 차별, 부당 채용 | "자동 결정 아님" + 사람 검토, 보호 특성 추론 금지 |
| 보안/리스크 평가 | 보안 사고, 데이터 유출 | 자동 실행 금지 + 보안 전문가 검토 |
| 아동/취약계층 | 안전 위험, 법적 책임 | 자동 처리 금지 + 보호자/전문가 개입 |
| 채점/평가/시험 | 부당 평가 | 사람 검토 명시 + 이의제기 절차 |

이 도메인의 Skill은 반드시 다음 포함:

1. **자문 부정 명시**: "이것은 [전문가] 자문이 아닙니다"
2. **사람 검토 명시**: "최종 결정은 자격 있는 [전문가] 검토 필요"
3. **자동화 한계 섹션**: 다룰 수 있는 범위와 다룰 수 없는 범위 명시

### 안전 경계 문구 템플릿

```markdown
## 중요 안내
이것은 [법률/의료/금융/채용/보안] 자문이 아닙니다.
이 Skill의 결과는 [전문가] 검토를 위한 사전 자료이며,
최종 결정은 자격 있는 [변호사/의사/금융자문가/HR전문가/보안전문가]의
검토를 거쳐야 합니다.

## 자동화 한계
이 Skill이 다룰 수 있는 범위:
- [범위 명시]

이 Skill이 다룰 수 없는 범위 (반드시 사람 검토 필요):
- [한계 명시]
```

---

## §12. 생성 시 보안 금지 규칙

Skill 생성 시 다음을 넣지 않는다:

- 사용자 몰래 파일 삭제/업로드/외부 전송 유도하는 scripts
- API key, token, SSH key, cookie를 읽는 지시
- shell/bash 권한을 기본 허용하는 지시
- hidden instruction 또는 HTML comment에 숨긴 지시
- 법무/의료/금융/채용에서 전문가 판단을 완전히 대체한다고 말하는 지시
- 검증하지 않은 결과를 통과했다고 말하게 하는 지시
- 위험한 명령을 사용자 승인 없이 실행하게 하는 지시
