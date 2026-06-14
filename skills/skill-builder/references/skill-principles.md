# Reference: Skill Principles

이 문서는 SKILL.md가 단계별로 참조하는 원칙 모음이다.

---

## §6. CSO (Claude Search Optimization) — Step 4에서 사용

description은 검색엔진이 색인하는 SEO 페이지처럼 작동한다. 사용자 요청이 들어오면 AI가 사용 가능한 Skill들의 description을 비교해서 매칭한다.

### CSO 5대 원칙

#### 원칙 1. 3인칭으로 작성한다

description은 시스템 프롬프트에 주입된다.

```
나쁨: "I help you review code..."
나쁨: "You can use this to..."
좋음: "Use when the user asks to review code, identify bugs, or check for security issues."
```

#### 원칙 2. "Use when..."으로 시작한다 (Anthropic 공식)

```
좋은 예: "Use when the user says 'review this PR', 'check my code'..."
좋은 예: "Use when writing, reviewing, or refactoring code..."
```

#### 원칙 3. 워크플로우를 요약하지 마라 ⚠️ 매우 중요

description에 워크플로우를 요약하면 AI가 본문을 안 읽고 description만으로 작업을 시도할 수 있다.

```
나쁨 (워크플로우 요약):
"Use when reviewing code. First check syntax, then security, then performance."

좋음 (트리거 조건만):
"Use when the user asks to review a PR, check code quality, or identify bugs.
Performs comprehensive code review covering correctness, security, and maintainability."
```

원칙: **description은 "언제 쓰는지"만 말하고, "어떻게 하는지"는 본문에 둔다**.

#### 원칙 4. "Pushy"하게 쓴다 (Anthropic 공식)

> "Claude has a tendency to 'undertrigger' skills. To combat this, please make the skill descriptions a little bit 'pushy'."

```
약함: "This skill can help with code reviews."
약함: "May be useful when reviewing code."
좋음: "Use when the user asks to review code. Always use this skill instead of providing ad-hoc review comments."
```

#### 원칙 5. 사용자가 실제로 입력할 표현을 포함한다

전문 용어가 아니라 자연스러운 표현, 한국어 사용자라면 한국어 트리거도 포함.

```
약함: "Use for code quality assurance procedures."
좋음: "Use when the user says 'review this PR', 'check my code', 'look for bugs', '코드 리뷰', '코드 검토', or asks to identify issues in code changes."
```

### Description 작성 공식

```
Use when [트리거 조건 + 사용자 표현 5~7개].
Also trigger when [추가 조건].
[1~2줄로 무엇을 하는 Skill인지 — 워크플로우 요약 금지].
[Pushy 강조: "Always use this skill instead of..."].
Do not use for [제외 조건 3개 이상].
```

### underTrigger와 overTrigger 모두 점검

- **underTrigger (false negative)**: 발동해야 하는데 안 됨 → "pushy"하게 보강
- **overTrigger (false positive)**: 발동하면 안 되는데 됨 → "Do not use" 조건 강화

---

## §7. 전문가급 Skill의 5대 요건

이 5가지를 모두 만족해야 "전문가급"이라고 부를 수 있다.

### 요건 1. 도메인 특이적 워크플로우

**전문가급:** 코드 리뷰 → 보안 / 성능 / 테스트 커버리지 / 유지보수성 4축
**일반론:** 코드를 꼼꼼히 살펴본다

### 요건 2. 판단 기준의 명시화

**전문가급:** "If you write 200 lines and it could be 50, rewrite it" (Karpathy)
**일반론:** "코드를 간결하게 작성한다"

### 요건 3. 흔한 실수의 도메인 맥락

**전문가급:** "결측치 처리 전에 평균을 계산하지 않는다 (결측치를 0으로 채우면 평균이 왜곡됨)"
**일반론:** "꼼꼼히 한다, 실수하지 않는다"

### 요건 4. 실행 가능한 검증 단계

**전문가급:** "린트와 테스트를 실제로 실행한다 (npm run lint && npm run test)"
**일반론:** "오류가 없는지 확인한다"

### 요건 5. 결과의 의사결정 가치

**전문가급:** Risk table (등급 + 권고 행동) + Negotiation points + Lawyer review items
**일반론:** 관찰한 내용 나열

---

## §8. Workflow 작성 5원칙

### 원칙 1. 동사로 시작 (명령형)

```
약함: "You should check the test results."
강함: "Check the test results."

약함: "If you want to add a chart, you can..."
강함: "To add a chart, use the chart tool."
```

### 원칙 2. 한 단계 = 한 가지 행동

```
좋음: "결측치, 중복, 이상치, 단위 문제를 점검한다."
나쁨: "데이터를 확인하고 정리한 후 분석을 시작하고 결과를 시각화한다."
```

### 원칙 3. 측정 가능한 완료 기준

```
좋음: "린트 명령을 실행해 에러 0개 확인"
나쁨: "코드 품질을 본다"
```

### 원칙 4. 의존 관계 순서 명확

```
좋음: "1. 데이터 품질 점검 → 2. 핵심 지표 정의 → 3. 분포 분석"
나쁨: 순서 없는 불릿 나열
```

### 원칙 5. 7±2 단계 적정 (5~9단계)

- 4단계 이하 → 일반론 위험
- 10단계 이상 → 단계 통합 또는 references/로 분리
- 메타-Skill (Karpathy 4원칙)은 4개도 OK

---

## §9. 2축 분류 (Process/Implementation × Rigid/Flexible) — Step 5에서 사용

### 1축: Process vs Implementation

| 구분 | 정의 | 예시 |
|---|---|---|
| Process | 일하는 방식 | TDD, debugging, brainstorming, karpathy-guidelines |
| Implementation | 특정 작업 수행 | cloud-deploy, frontend-design, budget-variance-analysis |

### 2축: Rigid vs Flexible

| 구분 | 정의 | 발동 후 행동 |
|---|---|---|
| Rigid | 규율(discipline)이 핵심 | 절대 적응 안 함. 예외 허용 안 함. |
| Flexible | 원칙을 맥락에 맞춰 적용 | 상황에 따라 조정 가능 |

### 4가지 조합과 작성 전략

| 조합 | 예시 | 작성 전략 |
|---|---|---|
| Process + Rigid | TDD, karpathy-guidelines, debugging | **합리화 차단(§10) 강력 적용. Iron Law.** |
| Process + Flexible | brainstorming, planning, decision-making | 판단 기준 + 체크리스트 |
| Implementation + Rigid | security-audit, compliance, 법무 | 단계별 절차. 검증 단계 필수. |
| Implementation + Flexible | frontend-design, copywriting | 원칙 + 예시. 도메인 판단 기준. |

### 메타-Skill (Process + Rigid의 특수형)

특징:
- 작업 자체가 아니라 "작업하는 방식" 교정
- 광범위 발동이 의도됨 (false positive가 정상)
- Workflow가 절차가 아니라 "원칙 체크리스트"
- 합리화 차단 필수

### 우선순위 규칙

여러 Skill 동시 발동 가능 시: **Process skills first, then Implementation skills**

---

## §10. Rigid Skill 작성법 — 합리화 차단 — Step 7에서 사용

### 합리화의 본질

> AI는 똑똑하다. 압박받으면 "loophole"을 찾아낸다.

흔한 합리화:
- "이건 예외 상황이야"
- "이번만은"
- "원칙의 spirit은 따랐어 (letter는 어겼지만)"
- "사용자가 빨리 해달라고 했으니까"
- "테스트 30분이면 충분해"

### Foundational Principle 추가

Rigid Skill에는 본문 앞쪽에 다음 한 줄을 둔다:

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

### 단순 진술이 아니라 워크어라운드 차단

```markdown
# 약함 (단순 진술)
- Always write tests first.

# 강함 (합리화 차단)
**Iron law: Tests first, code second. No exceptions.**

Write code before test? Delete it. Start over.
Edit code without testing? Same violation.
"Just this once"? Stop. That's rationalization.
"30 minutes of tests after"? Not TDD.
"The spec is obvious"? Then writing the test takes 30 seconds.
```

### Karpathy 스타일 강력한 구조

```markdown
## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**

## 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**

## 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
```

각 원칙 헤더 직후 굵은 한 줄짜리 iron law. 이게 Rigid Skill의 시그니처 형식.

### Rationalization Table

압박 테스트에서 발견된 합리화 패턴을 표로:

```markdown
## Rationalization Patterns to Reject

| 합리화 | 차단 |
|---|---|
| "이건 예외 상황" | 예외 없음. 규칙은 모든 경우에 적용. |
| "사용자가 급하다고 했으니" | 사용자 압박은 규율 완화 사유 아님. |
| "spirit은 지켰어" | Letter 위반은 spirit 위반. |
| "이번만은" | "Just this once"는 always의 시작. |
```

---

## §11. TDD for Skills — Step 11에서 사용

### TDD 매핑

| TDD 개념 | Skill 생성 |
|---|---|
| Test case | Pressure scenario (압박 시나리오) |
| Production code | SKILL.md |
| Test fails (RED) | Skill 없이 베이스라인 시나리오에서 AI 실패 |
| Test passes (GREEN) | Skill 적용 후 AI가 규칙 준수 |
| Refactor | 합리화 패턴 차단 |

### RED-GREEN-REFACTOR 사이클

#### RED 단계: 베이스라인 실패 관찰

Skill 쓰기 **전에**, 일반 프롬프트로 같은 작업을 시켜본다:
- AI가 어떻게 실패하는지 정확히 기록
- 어떤 합리화를 사용하는지 기록

핵심 원칙:
> "If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing."

#### GREEN 단계: 그 실패만 정확히 막는 Skill 작성

베이스라인에서 발견된 실패 패턴을 정확히 짚어 Skill 본문에 반영.

#### REFACTOR 단계: 합리화 패턴 차단

새로운 압박 시나리오로 재테스트 → AI가 빠져나가려 하는 새 loophole 발견 → 본문에 명시적으로 차단 추가 → 반복.

### Pressure Scenarios

AI가 규칙을 어기고 싶게 만드는 상황을 일부러 만든다.

7가지 압박 패턴:
- **시간 압박**: "급해. 데모가 1시간 남았어."
- **권위 압박**: "사용자가 명시적으로 면제했어."
- **일관성 압박**: "기존 코드도 안 따랐어."
- **단순함 압박**: "이건 그냥 한 줄짜리야."
- **예외 압박**: "이번만은 OK."
- **목적 압박**: "어차피 곧 버릴 코드야."
- **Spirit vs Letter**: "spirit은 지켰잖아."

각 시나리오에서 Skill이 규율을 유지하는지 확인. 무너지면 본문에 명시적 차단 추가.

### 20-Query Eval

description 발동 정확도를 정량 측정 (Anthropic 공식 권장):

```json
[
  {"query": "이 PR 리뷰해줘", "should_trigger": true},
  {"query": "보안 이슈 있는지 봐줘", "should_trigger": true},
  {"query": "이 변수명만 바꿔줘", "should_trigger": false},
  {"query": "오타 하나 고쳐줘", "should_trigger": false},
  ...
]
```

20개 (should/should-not 균형) → 새 세션 발동률 측정 → 90%+ 통과.

---

## §12. Common Mistakes / Gotchas / Troubleshooting 차이

| 구분 | 목적 | 시점 |
|---|---|---|
| Common Mistakes | 일반 실수 방지 | 사전, 일반적 |
| Gotchas | 치명적 함정 사전 방지 | 사전, 도메인 특이적 |
| Troubleshooting | 증상별 사후 해결 | 사후 |

**의도적 미니멀리즘**: 셋 중 일부만 넣어도 된다. Karpathy Guidelines는 Common Mistakes만 두고 Gotchas/Troubleshooting을 일부러 안 넣었다.

---

## §13. references/ 분리 기준

반드시 SKILL.md에 둘 것:
- 트리거 조건 (description)
- 핵심 워크플로우
- 검증 기준
- 출력 형식

references/로 분리할 것:
- 긴 예제
- 스타일가이드 전체
- 용어집
- 상세 평가표

원칙: AI는 references를 항상 읽지 않는다. 핵심은 SKILL.md 본문에 인라인.

**SKILL.md 길이**: 500줄 이내 (Anthropic 공식). 넘으면 references/로 분리, 본문에서 "When X, read references/Y.md" 명시.

---

## §15. "One Excellent Example" 원칙

```
❌ 5개 언어로 같은 예제
❌ 일반화된 fill-in-the-blank 템플릿
✅ 가장 적합한 언어 1개로 완전히 작동하는 예제
```

좋은 예제: Complete and runnable, well-commented, 실제 시나리오 기반, 그대로 사용 가능.
