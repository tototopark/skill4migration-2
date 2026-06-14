# Reference: Templates

이 문서는 Step 6, 10에서 SKILL.md 및 tests/prompts.md 작성 시 참조하는 템플릿 모음이다.

**중첩 코드블록 안전 처리**: 바깥은 ` ``` `, 안쪽 예시는 `~~~`로 차별화.

---

## §1. 일반 Skill 템플릿 (Implementation + Flexible)

```md
---
name: skill-name
description: Use when the user says "[trigger1]", "[trigger2]", "[한국어 트리거]", or asks to [specific task]. Also trigger when [추가 조건]. [Brief one-line of what this skill does — no workflow summary]. Always use this skill instead of [generic alternative]. Do not use for [exclusion1], [exclusion2], [exclusion3].
---

# [Skill 제목 — 사용자 언어로]

## Goal
[이 Skill의 목표 — 한 문장]

## Workflow
1. [동사로 시작하는 단계]
2. [동사로 시작하는 단계]
3. ...

## Domain Rules
- [도메인 특이적 판단 기준]

## Common Mistakes
- Do not [도메인 맥락의 실수].

## Verification Checklist
- [ ] [실행 가능한 검증]

## Output Format
1. [의사결정에 쓸 수 있는 출력 항목]
2. [출력 항목]
```

---

## §2. Rigid Skill 추가 템플릿 (Process + Rigid 또는 Implementation + Rigid)

위 §1 템플릿에 다음 섹션 추가:

```md
## Foundational Principle
**Violating the letter of the rules is violating the spirit of the rules.**

## Iron Laws
[각 원칙을 다음 형식으로]

### N. [원칙 제목]
**[한 줄 명령형]**

[설명]
[구체적 do/don't]

## Rationalization Patterns to Reject

| 합리화 | 차단 |
|---|---|
| "이건 예외" | 예외 없음. |
| "급해서" | 시간 압박은 규율 완화 사유 아님. |
| "spirit은 지켰어" | Letter 위반은 spirit 위반. |
| "이번만은" | Just this once는 always의 시작. |
| "다른 곳도 안 따랐어" | 일관성 압박은 사유 아님. |
```

---

## §3. 메타-Skill 추가 템플릿 (Process + Rigid의 특수형)

§2 Rigid 템플릿에 추가:

```md
## Scope of Application
This skill applies to all [작업 카테고리, 예: code writing, reviewing, refactoring].

## Why This Skill Exists
[해결하려는 흔한 실패 패턴 명시]
- [실패 1]
- [실패 2]
- [실패 3]

## When NOT to Apply
[의도적 광범위 발동이지만 명백한 예외만 명시]
- Trivial single-line edits where caution overhead exceeds benefit
```

---

## §4. 고위험 도메인 추가 섹션

§1 또는 §2 템플릿에 추가:

```md
## 중요 안내
이것은 [법률/의료/금융/채용] 자문이 아닙니다.
최종 결정은 자격 있는 [전문가] 검토가 필요합니다.

## 자동화 한계
- 이 Skill이 다룰 수 있는 범위: [...]
- 반드시 사람이 검토해야 하는 항목: [...]
```

---

## §5. tests/prompts.md 템플릿

```md
# Test Prompts for [skill-name]

## 1. Should trigger
표준 발동 시나리오.

예시 요청:
~~~
[표준 요청]
~~~

## 2. Should not trigger
명백한 비대상.

예시 요청:
~~~
[비대상 요청]
~~~

## 3. Adversarial trigger
트리거 단어 포함, 발동 안 돼야 함.

예시 요청:
~~~
[Adversarial 요청]
~~~

## 4. Cross-domain confusion
비슷한 다른 Skill과 헷갈림.

예시 요청:
~~~
[헷갈림 요청]
~~~

## 5. Missing inputs
필수 정보 빠짐.

예시 요청:
~~~
[정보 부족 요청]
~~~

## 6. Realistic complex
실제 업무 복잡 요청.

예시 요청:
~~~
[복잡 요청]
~~~

## 7. Edge or failure
엣지/실패 케이스.

예시 요청:
~~~
[엣지 요청]
~~~

## 8. Pressure Scenarios (Rigid Skill 전용)

### 시간 압박
~~~
[급해, 빨리 해줘 형식]
~~~

### 권위 압박
~~~
[사용자가 명시적으로 면제 형식]
~~~

### 일관성 압박
~~~
[기존도 안 따랐어 형식]
~~~

### 단순함 압박
~~~
[이건 그냥 한 줄 형식]
~~~

### 예외 압박
~~~
[이번만은 OK 형식]
~~~

### 목적 압박
~~~
[곧 버릴 코드 형식]
~~~

### Spirit vs Letter
~~~
[spirit은 지켰잖아 형식]
~~~
```

---

## §6. Karpathy Guidelines 스타일 메타-Skill 예시

전체 구조 참고용:

```md
---
name: karpathy-guidelines
description: Use when writing, reviewing, or refactoring code. Behavioral guidelines to reduce common LLM coding mistakes — surfacing assumptions, simplicity-first, surgical changes, and verifiable success criteria. Always use this skill for any non-trivial code task. Do not use for typo-only edits, comment-only changes, or trivial single-line fixes where caution overhead exceeds benefit.
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## Foundational Principle
**Violating the letter of the rules is violating the spirit of the rules.**

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- If you write 200 lines and it could be 50, rewrite it.

Test: "Would a senior engineer say this is overcomplicated?"

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals.
```

---

## §7. Description 작성 좋은/나쁜 예시 모음

### Implementation + Flexible (코드 리뷰)

❌ 나쁨:
```
description: Helps with code reviews.
```

✅ 좋음:
```
description: Use when the user says "review this PR", "check my code", "look for bugs", "코드 리뷰", "코드 검토", or asks to identify issues in code changes. Always use this skill instead of providing ad-hoc review comments. Do not use for typo-only edits, comment-only changes, or simple variable renames.
```

### Process + Rigid (TDD)

❌ 나쁨:
```
description: TDD skill. Always test first.
```

✅ 좋음:
```
description: Use when implementing new features, fixing bugs, or making any behavior-changing code modifications. Enforces strict red-green-refactor TDD cycle. Always use this skill for production code changes. Do not use for documentation-only edits, comment changes, or experimental prototypes explicitly marked as throwaway.
```

### 메타-Skill (Karpathy Guidelines)

✅ 좋음 (의도적 광범위 발동):
```
description: Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria. Always use this skill for any non-trivial code task. Do not use for typo-only edits or trivial fixes.
```

### 고위험 도메인 (법무)

✅ 좋음 (안전 경계 명시):
```
description: Use when the user says "계약서 검토", "리스크 분석", "contract review", "NDA 검토", or asks to identify risks in a contract. NOT legal advice — produces preliminary review for lawyer's final review. Always use this skill instead of providing casual contract opinions. Do not use for contract drafting, dispute strategy, or any matter requiring qualified legal counsel.
```

---

## §8. SKILL.md 길이 가이드

| Skill 유형 | 권장 길이 | 비고 |
|---|---|---|
| 메타-Skill (Karpathy 스타일) | 50~150줄 | 의도적 미니멀리즘 |
| 일반 Implementation | 150~350줄 | 표준 길이 |
| 복잡한 Process Skill (TDD 등) | 300~500줄 | 합리화 차단 포함 |
| 도메인 특화 Implementation | 200~450줄 | references/ 분리 권장 |

500줄 초과 시:
- 핵심 워크플로우는 SKILL.md 본문 유지
- 긴 예제, 도메인 용어집, 상세 평가표는 references/로 분리
- 본문에서 "When X, read references/Y.md"로 명시 안내
