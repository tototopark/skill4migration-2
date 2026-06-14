---
name: skill-builder
description: Use when the user says "스킬 만들어줘", "Skill 만들어줘", "create a skill", "make me a skill", "스킬 생성", "에이전트 스킬", "agent skill", or asks to design a new SKILL.md, generate Skill files, or create reusable AI agent workflows. Always use this skill instead of providing ad-hoc skill drafts. This skill produces production-quality skills following CSO, 2-axis classification, and TDD-for-Skills patterns from validated popular skills like obra/superpowers and karpathy-guidelines. Do not use for editing unrelated files, generating code unrelated to skills, or providing general advice about prompt engineering.
license: MIT
---

# Skill Builder — 전문가급 Skill 생성기

검증된 인기 Skill의 패턴을 통합하여 Claude 데스크톱에 즉시 등록 가능한 Skill을 만든다.

## When to Use

이 Skill은 다음 상황에서 사용한다:
- 사용자가 "스킬 만들어줘", "Skill 만들어줘" 같은 요청
- 반복적인 AI 작업 패턴을 SKILL.md로 정리하려 할 때
- 기존 SKILL.md를 개선/리팩터링하려 할 때
- 외부 Skill을 보안 감사하려 할 때

## Foundational Principle

**Violating the letter of the rules is violating the spirit of the rules.**

이 Skill은 검증된 패턴을 따른다. "그냥 빨리 만들어줘", "이번만 짧게" 같은 합리화에 굴복하면 평범한 Skill이 만들어진다. 단계를 건너뛰지 않는다.

## Iron Law: References Are Mandatory Reading

**각 Step에 명시된 references 파일은 반드시 읽고 적용한다. "이미 알고 있다"는 합리화를 거부한다.**

이 SKILL.md 본문은 핵심 워크플로우만 다룬다. 도메인별 구체 절차, CSO 5대 원칙 상세, Rigid Skill 합리화 차단 작성법, 14개 도메인 패턴, 정확한 템플릿은 references/ 안에 있다. 본문만 읽고 진행하면 일반론이 만들어진다.

각 Step 시작 시:
1. ⚠️ **"이 단계 시작 전 반드시 읽는다"** 박스를 먼저 본다
2. 박스에 명시된 references 파일을 실제로 읽는다 (skim 아님, 해당 섹션 전체 읽기)
3. 읽은 내용을 적용한다
4. Verification Checklist Part A에서 독해 여부를 자가 확인한다

읽지 않으면 발생하는 결과:
- domain-patterns.md 안 읽음 → 일반론 워크플로우 (전문가급 5대 요건 1번 위반)
- skill-principles.md §6 안 읽음 → 약한 description (Skill이 발동 안 됨)
- skill-principles.md §10 안 읽음 → Rigid Skill이 Rigid가 아님
- templates.md 안 읽음 → 카테고리 누락 또는 형식 오류
- operations-security.md §11 안 읽음 → 고위험 도메인 안전 경계 누락 (사용자 손해)

## Core Workflow — 13단계

⚠️ **각 단계는 독립적이며 순서대로 진행한다.** 단계를 합치거나 건너뛰지 않는다. **각 Step의 "반드시 읽는다" 박스를 먼저 확인한다.**

### Step 1. 6단계 인터뷰 진행

명확한 요청이어도 단계별 확인을 거친다. 사용자가 "유튜브 제목 최적화 스킬 만들어줘"처럼 명확하게 말해도, 다음 6단계를 모두 거친다.

각 단계는 한 번에 하나의 질문을 한다. 한 번에 다 묻지 않는다.

#### 1.1 도메인 대분류

```
좋습니다. 어떤 종류의 작업을 자동화하고 싶으신가요?

A. 코드/기술 — 개발, 데이터 분석, 보안, 자동화
B. 글/콘텐츠 — 문서 작성, 마케팅, 유튜브, 카피
C. 비즈니스 — 재무, 제품기획, 경영기획, HR
D. 검토/판단 — 법무, 디자인 리뷰, 교육/코칭
E. 멀티 에이전트 — 여러 전문가 관점 조율
F. 메타-Skill — AI의 작업 방식 자체를 교정
G. 기타: 직접 입력
```

명확한 요청이 있다면 추정 답을 제시하면서 확인:
> "유튜브 제목 최적화는 'B. 글/콘텐츠'로 보입니다. 맞나요?"

#### 1.2 세부 도메인

대분류에 맞춰 세부 옵션 5~6개 제시. references/domain-patterns.md 참조.

#### 1.3 작업 유형

```
이 Skill이 주로 처리할 작업은?
A. 리뷰/검토  B. 작성/생성  C. 분석/진단  D. 요약/정리
E. 변환/재구성  F. 자동화 설계  G. 의사결정 지원
H. 행동 가이드라인 (메타-Skill)  I. 기타
```

#### 1.4 결과물 형태

```
어떤 산출물을 받고 싶으세요?

A. ⭐ Claude 데스크톱 등록용 패키지 (권장 기본값)
   → SKILL.md + tests/prompts.md + ZIP 만드는 법 + 5단계 등록 가이드
B. 텍스트만 (직접 정리하실 분용)
C. GitHub 공유용 (README, LICENSE 추가)
D. 기존 SKILL.md 개선/리팩터링
E. 외부 Skill 보안 감사
F. 기타
```

#### 1.5 2축 분류 자동 판정

인터뷰 결과를 바탕으로 사용자에게 분류 결과를 보여주고 확인받는다:

```
[2축 분류 판정]
- 1축: [Process / Implementation]
- 2축: [Rigid / Flexible]
- 종합 유형: [예: Implementation + Flexible]
- 적용 작성 전략: [references/skill-principles.md §9 참조]

이대로 진행할까요?
```

판정 가이드:
- "AI 자체의 동작을 교정" → Process + Rigid (메타-Skill)
- "TDD, debugging, 보안 감사" → Process+Rigid 또는 Implementation+Rigid
- "법무, HR, 채용" → Implementation + Rigid (고위험)
- "코드 리뷰, 문서 작성, 마케팅" → Implementation + Flexible

#### 1.6 추가 정보 (필요 시)

- 사용 환경 (혼자 / 팀 / 공개)
- 고위험 여부
- Pressure Scenarios 필요 여부 (Rigid는 자동 ON)

### Step 2. 고위험 도메인 판정

⚠️ **이 단계 시작 전 반드시 읽는다:**
- `references/operations-security.md` 의 §11 (고위험 도메인 정의와 안전 경계)
- `references/operations-security.md` 의 §12 (생성 시 보안 금지 규칙)

**파일을 읽지 않고 진행하면 안전 경계 누락 가능. 법무/의료/금융/채용/보안 도메인에서 자문 부정 명시 + 사람 검토 명시 + 자동화 한계 섹션이 빠지면 사용자에게 직접적 손해를 끼칠 수 있다.**

다음 중 하나라도 해당하면 고위험으로 분류:
- 법무/계약, 의료/건강, 금융/투자
- 채용/인사 결정
- 보안/리스크 평가
- 아동/취약계층 관련
- 채점/평가/시험

고위험이면 SKILL.md에 "자문 부정 명시" + "사람 검토 명시" + "자동화 한계" 섹션 필수.

상세 안전 경계 문구 템플릿은 **references/operations-security.md §11** 에서 확인.

### Step 3. name 결정

규칙:
- lowercase kebab-case
- 도메인-작업-결과물 패턴
- 일반적이지 않게 (예: `coding-skill` ❌, `code-review-quality-gate` ✅)

### Step 4. ⭐ Description 작성 (CSO 5대 원칙)

⚠️ **이 단계 시작 전 반드시 읽는다:**
- `references/skill-principles.md` 의 §6 (CSO 5대 원칙 전문)
- `references/templates.md` 의 §7 (Description 작성 좋은/나쁜 예시 모음)

**파일을 읽지 않고 진행하면 description이 약해진다. CSO 5대 원칙 중 하나라도 빠지면 Skill이 발동 안 되거나 잘못 발동한다. 특히 원칙 3 (워크플로우 요약 금지)을 모르고 진행하면 AI가 본문을 안 읽는 Skill이 만들어진다.**

**가장 중요한 단계.** 잘못 쓰면 Skill이 발동되지 않는다.

5대 원칙:
1. "Use when..."으로 시작
2. 3인칭으로 작성
3. **워크플로우를 요약하지 마라** (요약하면 AI가 본문을 안 읽음)
4. **"Pushy"하게 쓴다** (undertrigger 방어 — Anthropic 공식)
5. 사용자가 실제로 입력할 표현 5~7개 포함 (한국어/영어 혼합)

공식:
```
Use when [트리거 조건 + 사용자 표현 5~7개 + 한국어/영어 혼합].
Also trigger when [추가 조건].
[1~2줄로 무엇을 하는 Skill인지 — 워크플로우 요약 금지].
[Pushy 강조: "Always use this skill instead of..."].
Do not use for [제외 조건 3개 이상].
```

상세 원칙과 예시는 **references/skill-principles.md §6** 와 **references/templates.md §7** 에서 확인.

### Step 5. 2축 분류에 따른 작성 전략 적용

⚠️ **이 단계 시작 전 반드시 읽는다:**
- `references/skill-principles.md` 의 §9 (2축 분류 — Process/Implementation × Rigid/Flexible)

**4가지 조합마다 작성 전략이 다르다. 분류만 명시하고 작성 전략을 적용하지 않으면 분류한 의미가 없다. 특히 Process+Rigid (메타-Skill)는 합리화 차단이 핵심인데 이걸 빼먹으면 Rigid가 안 된다.**

| 종합 유형 | 작성 전략 |
|---|---|
| Process + Rigid (메타-Skill 포함) | 합리화 차단 강력 적용. 단호한 명령형. Iron Law. |
| Process + Flexible | 판단 기준과 체크리스트. 맥락별 분기. |
| Implementation + Rigid | 단계별 절차. 검증 단계 필수. |
| Implementation + Flexible | 원칙 + 예시. 도메인 판단 기준. |

### Step 6. Workflow 작성

⚠️ **이 단계 시작 전 반드시 읽는다:**
- `references/domain-patterns.md` 의 [Step 1.2에서 선택한 도메인 번호] 섹션 전체
- `references/skill-principles.md` 의 §8 (Workflow 작성 5원칙)

**파일을 읽지 않고 진행하면 일반론이 작성된다. 도메인 특이적 워크플로우 5대 요건(요건 1)을 위반한다. 14개 도메인 모두 도메인 전문가가 실제로 따르는 절차가 명시되어 있고, 그것을 따라야 "전문가급"이라고 부를 수 있다.**

**도메인별 구체적 워크플로우는 references/domain-patterns.md를 읽어 적용한다.** 14개 도메인 모두 거기에 있다.

5원칙:
1. 동사로 시작 (명령형)
2. 한 단계 = 한 행동
3. 측정 가능한 완료 기준
4. 의존 관계 순서 명확
5. 5~9단계 적정 (메타-Skill은 4개도 OK)

### Step 7. ⭐ Rigid Skill인 경우 — 합리화 차단 추가

⚠️ **이 단계 시작 전 반드시 읽는다 (Rigid Skill인 경우):**
- `references/skill-principles.md` 의 §10 (Rigid Skill 작성법 — 합리화 차단)
- `references/templates.md` 의 §2 (Rigid Skill 추가 템플릿)
- `references/templates.md` 의 §6 (Karpathy Guidelines 스타일 메타-Skill 예시 전체 구조)

**파일을 읽지 않고 진행하면 Rigid가 안 된다. AI는 압박받으면 "loophole"을 찾아낸다. 합리화 패턴을 명시적으로 호명하고 차단하지 않으면 Skill이 무의미해진다. Iron Law 형식 (한 줄 명령형 굵게)을 정확히 따라야 시그니처 형식이 된다.**

Rigid Skill (Process+Rigid 또는 Implementation+Rigid)이면 다음을 본문에 포함:

1. **Foundational Principle 한 줄**:
   ```
   **Violating the letter of the rules is violating the spirit of the rules.**
   ```

2. **각 원칙을 Iron Law 형식으로** (Karpathy 스타일):
   ```
   ## N. [원칙 제목]
   **[한 줄 명령형 - 굵게]**
   [설명 + 구체적 do/don't]
   ```

3. **합리화 패턴 명시적 차단** (5개 이상):
   - "이건 예외야"? 예외 없음.
   - "급해서"? 시간 압박은 규율 완화 사유 아님.
   - "spirit은 지켰어"? Letter 위반은 spirit 위반.
   - "이번만은"? Just this once는 always의 시작.
   - "다른 곳도 안 따랐어"? 일관성 압박은 사유 아님.

4. **Rationalization Table** (선택)

상세 합리화 차단 작성법은 **references/skill-principles.md §10** 에서 확인.
완전한 예시 구조는 **references/templates.md §6** (Karpathy Guidelines 스타일)에서 확인.

Flexible Skill이면 이 단계 건너뛴다.

### Step 8. Domain Rules / Common Mistakes / Output Format

⚠️ **이 단계 시작 전 반드시 읽는다:**
- `references/skill-principles.md` 의 §7 (전문가급 Skill의 5대 요건)

**5대 요건을 모두 만족해야 "전문가급"이라고 부를 수 있다. 단순히 모든 섹션을 채웠다고 전문가급이 되지 않는다. 일반론과 전문가급의 차이가 §7에 구체 예시로 비교되어 있으니 반드시 확인.**

전문가급 5대 요건 점검:
- 도메인 특이적 워크플로우
- 판단 기준 명시
- 도메인 맥락의 흔한 실수
- 실행 가능한 검증
- 의사결정 가치

### Step 9. Verification Checklist 작성

실행 가능한 체크. 추상적 ❌ → 명령으로 검증 가능 ✅.

### Step 10. 테스트 프롬프트 7~8개 카테고리

⚠️ **이 단계 시작 전 반드시 읽는다:**
- `references/templates.md` 의 §5 (tests/prompts.md 템플릿)

**파일을 읽지 않고 진행하면 7개 카테고리의 정확한 형식을 따르지 못한다. 특히 Rigid Skill의 Pressure Scenarios 7가지 패턴 (시간/권위/일관성/단순함/예외/목적/Spirit-vs-Letter)은 templates.md §5의 정확한 구조를 따라야 한다.**

기본 7개:
1. Should trigger
2. Should not trigger
3. Adversarial trigger (트리거 단어 포함, 발동 안 돼야 함)
4. Cross-domain confusion
5. Missing inputs
6. Realistic complex
7. Edge or failure

**Rigid Skill 추가 카테고리 (필수):**
8. Pressure Scenarios 5~7개 (시간/권위/일관성/단순함/예외/목적/Spirit-vs-Letter 압박)

상세 템플릿은 **references/templates.md §5** 에서 확인.

### Step 11. TDD for Skills 검증 절차 안내

⚠️ **이 단계 시작 전 반드시 읽는다:**
- `references/skill-principles.md` 의 §11 (TDD for Skills)

**파일을 읽지 않고 진행하면 검증 절차의 핵심을 놓친다. RED 단계 (베이스라인 실패 관찰)는 단순히 "Skill 없이 한번 해봐"가 아니라 "AI가 어떻게 실패하는지 정확히 기록"이다. 이걸 모르면 검증 절차가 형식적으로 끝난다.**

사용자에게 RED-GREEN-REFACTOR 사이클 안내:

```
1. RED — 베이스라인 실패: Skill 없이 시나리오 실행, AI 실패 패턴 관찰
2. GREEN — Skill 적용 검증: 같은 시나리오에서 통과 확인
3. REFACTOR — 합리화 차단 (Rigid): Pressure Scenarios로 재테스트
4. (선택) 20-Query Eval: should/should-not 10개씩 → 90% 정확도 확인
```

상세는 **references/skill-principles.md §11** 에서 확인.

### Step 12. 30문항 자가검증

다음 30개 항목을 모두 점검 (각 ✅/❌):

기본 구조 (4문항):
1-4. name 형식, description "Use when..." 시작, 3인칭, 충돌 없음

CSO 원칙 (5문항):
5-9. 워크플로우 미요약, Pushy, 영어+한국어 트리거, Do not use 3개+, 실제 표현

2축 분류 (3문항):
10-12. 유형 명시, 작성 전략 일치, 메타-Skill 광범위 발동 의도

도메인 적합성 (3문항):
13-15. 도메인 특이적, 동사 시작, 5~9단계

Rigid Skill 합리화 차단 (3문항):
16-18. Foundational Principle, Iron Law, 합리화 5개+ 차단

품질 보호 (3문항):
19-21. Common Mistakes 도메인 맥락, Verification 실행 가능, Output 의사결정 가치

TDD for Skills (3문항):
22-24. 7개 카테고리, Pressure Scenarios (Rigid), RED-GREEN-REFACTOR 안내

안전성 (2문항):
25-26. 고위험 안전 경계, 보안 금지 위반 없음

Claude 데스크톱 등록 (4문항):
27-30. 폴더 구조, SKILL.md 위치, 5단계 가이드, 4단계 발동 검증

**통과 기준**: 30개 중 28개 이상 ✅. Rigid는 16-18, 22-24 모두 ✅ 필수.

### Step 13. ⭐ Claude 데스크톱 등록 패키지 출력

자가검증 통과 후, 사용자가 받는 최종 출력:

#### 13.1 폴더 구조 텍스트로 출력

Skill 유형에 따라 필요한 폴더만:

**기본 (모든 Skill)**:
```
{skill-name}/
├── SKILL.md
└── tests/
    └── prompts.md
```

**조건부 추가 폴더** (필요한 경우만):
- `scripts/`: 결정론적 코드 실행 필요 시
- `references/`: 본문 500줄 초과 가능성 시
- `assets/`: 출력물 템플릿/이미지 필요 시

#### 13.2 사용자가 ZIP 만드는 방법 안내

**Mac/Linux:**
```bash
# 1. 폴더 만들기
mkdir -p {skill-name}/tests

# 2. SKILL.md 저장
# (위 SKILL.md 내용을 {skill-name}/SKILL.md에 저장)

# 3. tests/prompts.md 저장
# (위 tests/prompts.md 내용을 {skill-name}/tests/prompts.md에 저장)

# 4. ZIP 압축
zip -r {skill-name}.zip {skill-name}/
```

**Windows:**
```
1. 탐색기에서 {skill-name} 폴더 만들기
2. 폴더 안에 tests 하위폴더 만들기
3. SKILL.md를 {skill-name}/ 안에 저장
4. tests/prompts.md를 {skill-name}/tests/ 안에 저장
5. {skill-name} 폴더 우클릭 → 보내기 → 압축(ZIP) 폴더
```

#### 13.3 Claude 데스크톱 등록 5단계

```
[등록 전 확인]
☐ Settings > Features에서 "Code execution and file creation" → ON

[5단계 등록]
1️⃣ Claude 데스크톱 앱을 엽니다.
2️⃣ 좌측 하단 프로필 아이콘 → "Settings" 클릭
3️⃣ 좌측 메뉴 "Customize" → "Skills" 선택
4️⃣ 우측 상단 "+" 버튼 → "+ Create skill" 클릭
5️⃣ 만든 ZIP 파일 업로드 → 토글 ON
```

#### 13.4 발동 검증 4단계

새 대화창에서 tests/prompts.md의 프롬프트 입력:
- ✅ Should trigger 테스트 → 자동 발동 확인
- ❌ Should NOT trigger 테스트 → 발동 안 됨 확인
- 🛡️ Adversarial 테스트 → false positive 방어 확인
- 🔥 Pressure Scenarios (Rigid) → 규율 유지 확인

#### 13.5 발동 실패 디버깅 표

| 증상 | 해결 |
|---|---|
| Skill 메뉴가 안 보임 | Settings > Features > Code execution ON |
| ZIP 업로드 후 목록에 없음 | ZIP 안에 {skill-name}/ 폴더 구조 확인 |
| 토글 켰는데 발동 안 됨 | 새 대화창 + 토글 OFF→ON 재설정 |
| 한국어 요청에 안 발동 | description에 한국어 트리거 추가 |
| 다른 Skill이 발동 | description의 차별화 강화 |
| 코드 실행 안 됨 | Settings > Features > Code execution ON |

상세는 **references/desktop-install-guide.md** 참조.

## Common Mistakes

- **인터뷰를 건너뛰지 마라.** 명확해 보여도 6단계 모두 거친다.
- **description에 워크플로우를 요약하지 마라.** AI가 본문을 안 읽는다.
- **Rigid Skill에 합리화 차단을 빼먹지 마라.** Iron Law 없이는 Rigid가 안 된다.
- **references/를 핵심 내용으로 채우지 마라.** 핵심은 SKILL.md 본문에.
- **Pressure Scenarios를 형식적으로 만들지 마라.** AI가 진짜 어기고 싶게 만들어야 한다.
- **30문항 자가검증을 형식적으로 통과하지 마라.** 한 항목씩 진짜 점검한다.

## Rationalization Patterns to Reject

| 합리화 | 차단 |
|---|---|
| "사용자가 명확하게 요청했으니 인터뷰 생략" | 명확해도 6단계 거친다. 사용자 의도 추정은 위험하다. |
| "이건 간단한 Skill이니 자가검증 일부만" | 30문항 모두 점검한다. 통과 기준은 28+. |
| "references는 나중에 만들지 뭐" | 메인 SKILL.md에서 명시 안내한 references는 같이 만든다. |
| "데스크톱 등록 가이드는 사용자가 알 거야" | 5단계는 매번 명시한다. 사용자가 안다고 가정하지 않는다. |
| **"이 도메인은 내가 잘 알아 references 안 봐도 돼"** | **references 안 읽으면 일반론. 14개 도메인 워크플로우는 무조건 읽고 적용한다. domain-patterns.md를 안 읽고 만든 워크플로우는 전문가급 5대 요건 1번 (도메인 특이적)을 위반한다.** |
| **"CSO 원칙은 외웠으니 skill-principles.md §6 안 읽어도 됨"** | **외운 게 아니라 적용해야 한다. 5대 원칙 중 하나라도 빠지면 description이 약해진다. 매번 §6를 열어 5개 모두 점검한다.** |
| **"Rigid Skill 합리화 차단 패턴은 익숙해"** | **§10을 안 읽고 진행하면 Iron Law 형식이 흐려진다. 합리화 패턴은 매번 다르고 새로 발견된다. Karpathy 스타일 시그니처 형식을 정확히 따른다.** |
| **"templates.md 안 읽어도 형식은 알겠어"** | **7개 카테고리 + Pressure Scenarios 정확한 형식은 templates.md에만 있다. 추측해서 만들면 카테고리 누락이나 형식 오류가 생긴다.** |

## Output Format

최종 출력 구조:

```
✅ Skill 생성 완료

[가정한 요구사항]
- 도메인 / 세부 영역 / 작업 유형
- 2축 분류 / 메타-Skill 여부
- 사용 환경 / 고위험 여부

[Skill 폴더 구조]
{skill-name}/
└── ...

[SKILL.md 내용]
(전체 내용)

[tests/prompts.md 내용]
(7~8개 카테고리)

[ZIP 만드는 방법]
(Mac/Linux + Windows 안내)

[Claude 데스크톱 등록 5단계]
1️⃣ ~ 5️⃣

[발동 검증 4단계]
✅ ❌ 🛡️ 🔥

[발동 실패 디버깅 표]

[자가검증 결과]
- 30개 항목 통과: [N/30]
- 미통과 항목: [목록]
- 추가 검토 필요: [목록]

[개선 가능 포인트]
```

## References

이 Skill의 본문은 핵심 워크플로우만 다룬다. 다음 reference 파일을 단계에 맞춰 읽어 적용한다:

- **references/skill-principles.md** — Step 4 (CSO), Step 7 (합리화 차단), Step 11 (TDD)에서 읽음
- **references/domain-patterns.md** — Step 6 (Workflow 작성)에서 도메인에 맞춰 읽음
- **references/operations-security.md** — Step 2 (고위험 판정)에서 읽음
- **references/desktop-install-guide.md** — Step 13.5 (디버깅) 상세 시 읽음
- **references/templates.md** — Step 6, 10에서 SKILL.md 및 tests/prompts.md 템플릿 참조

## Verification Checklist

### Part A — references 독해 확인 (먼저 체크)

⚠️ **이 섹션은 가장 먼저 점검한다. references를 안 읽었으면 다른 항목 점검은 무의미하다.**

생성 과정에서 다음 references를 실제로 읽었는가:
- [ ] **Step 2** (고위험 판정) → `references/operations-security.md` §11, §12 읽었는가?
- [ ] **Step 4** (Description CSO) → `references/skill-principles.md` §6 읽었는가?
- [ ] **Step 4** (Description CSO) → `references/templates.md` §7 (Description 예시 모음) 읽었는가?
- [ ] **Step 5** (2축 분류) → `references/skill-principles.md` §9 읽었는가?
- [ ] **Step 6** (Workflow) → `references/domain-patterns.md` 의 해당 도메인 섹션 읽었는가?
- [ ] **Step 6** (Workflow) → `references/skill-principles.md` §8 (Workflow 5원칙) 읽었는가?
- [ ] **Step 7** (Rigid 합리화 차단, 해당 시) → `references/skill-principles.md` §10 읽었는가?
- [ ] **Step 7** (해당 시) → `references/templates.md` §2, §6 읽었는가?
- [ ] **Step 8** (Domain Rules) → `references/skill-principles.md` §7 (5대 요건) 읽었는가?
- [ ] **Step 10** (테스트 프롬프트) → `references/templates.md` §5 읽었는가?
- [ ] **Step 11** (TDD) → `references/skill-principles.md` §11 읽었는가?

**한 항목이라도 ❌면 해당 Step을 다시 진행한다. references를 안 읽고 진행한 부분은 일반론으로 작성됐을 가능성이 높다.**

### Part B — 결과물 품질 확인

생성한 Skill이 다음을 모두 만족하는가:
- [ ] 30문항 자가검증 28+ 통과
- [ ] description이 "Use when..."으로 시작
- [ ] description이 워크플로우를 요약하지 않음
- [ ] description이 영어/한국어 트리거 모두 포함
- [ ] 2축 분류가 명시됨
- [ ] 도메인 특이적 워크플로우 (일반론 아님 — domain-patterns.md 적용 결과)
- [ ] Rigid Skill인 경우 Foundational Principle + Iron Law + 합리화 차단 포함
- [ ] 테스트 프롬프트 7개 카테고리 모두 있음 (templates.md §5 형식 따름)
- [ ] Rigid Skill인 경우 Pressure Scenarios 5+ (7가지 패턴 적용)
- [ ] 데스크톱 등록 5단계 가이드 출력에 포함
- [ ] 발동 검증 4단계 가이드 출력에 포함
- [ ] 발동 실패 디버깅 표 출력에 포함

**Part A와 Part B 모두 통과해야 최종 출력 가능.**

## License

MIT
