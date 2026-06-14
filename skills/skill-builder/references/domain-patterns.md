# Reference: Domain Patterns

이 문서는 14개 도메인의 전문가 워크플로우를 다룬다. Step 6 (Workflow 작성)에서 해당 도메인 부분만 읽어 적용한다.

각 도메인은 다음 구성:
- 대표 Skill
- Skill 유형 (2축 분류)
- 필수 입력값
- 전문가 워크플로우 (5~9단계)
- Gotchas
- 출력 형식

---

## 1. 소프트웨어 개발

대표 Skill: code-review-quality-gate, test-driven-development, bug-investigation, release-readiness-check

Skill 유형:
- code-review-quality-gate → Implementation + Flexible
- test-driven-development → Process + Rigid (합리화 차단 강력 적용)

필수 입력값: 변경 목적, 관련 코드, 기대 동작, 테스트 명령, 제약조건

전문가 워크플로우:
1. 요청을 기능 추가/버그 수정/리팩터링/문서화/테스트 보강 중 하나로 분류한다.
2. 변경 목적과 기대 동작을 확인한다.
3. 관련 파일과 기존 패턴을 확인한다.
4. 변경 범위를 최소 단위로 나눈다.
5. 가능하면 테스트를 먼저 작성하거나 기존 테스트를 확인한다.
6. 최소 변경으로 구현한다.
7. 타입 검사, 린트, 테스트, 빌드를 실행한다.
8. 변경 파일, 검증 결과, 남은 리스크를 요약한다.

Gotchas:
- 테스트를 실제로 실행하지 않았다면 통과했다고 말하지 않는다.
- 새 의존성은 승인 없이 추가하지 않는다.
- 관련 없는 파일을 대규모 수정하지 않는다.
- package.json 확인 없이 명령어를 invent하지 않는다.

출력: 요약 / 변경 파일 / 구현 내용 / 테스트·검증 결과 / 리스크 / 다음 작업

---

## 2. 데이터 분석

대표 Skill: exploratory-data-analysis-report, data-quality-check, dashboard-insight-review

Skill 유형: Implementation + Flexible

필수 입력값: 데이터, 분석 목적, 컬럼 설명, 기간, 비교 기준

전문가 워크플로우:
1. 분석 질문을 명확히 한다.
2. 데이터 구조와 컬럼 의미를 확인한다.
3. 결측치, 중복, 이상치, 단위 문제를 점검한다.
4. 핵심 지표를 정의한다.
5. 비교 기준을 설정한다.
6. 분포, 추세, 세그먼트 차이를 분석한다.
7. 이상치와 가능한 원인을 분리한다.
8. 인사이트와 한계를 분리해 보고한다.

Gotchas:
- 상관관계를 인과관계처럼 말하지 않는다.
- 결측치 확인 없이 결론 내지 않는다.
- 단위가 다른 값을 평균내지 않는다.
- 데이터 한계를 반드시 표시한다.

출력: Executive summary / 데이터 개요 / 데이터 품질 이슈 / 주요 패턴 / 이상치·리스크 / 해석과 한계 / 다음 행동

---

## 3. 문서 작성

대표 Skill: executive-summary-writer, business-proposal-editor, meeting-notes-summarizer

Skill 유형: Implementation + Flexible

필수 입력값: 원문, 문서 목적, 독자, 톤, 분량 제한

전문가 워크플로우:
1. 문서의 목적과 독자를 확인한다.
2. 핵심 메시지를 한 문장으로 정리한다.
3. 현재 구조가 목적에 맞는지 확인한다.
4. 중복, 비약, 모호한 표현을 제거한다.
5. 근거와 예시가 충분한지 확인한다.
6. 독자가 해야 할 다음 행동을 명확히 한다.

Gotchas:
- 원문에 없는 내용을 추가하지 않는다.
- 결론을 뒤로 미루지 않는다.
- 결정사항과 논의사항을 섞지 않는다.

출력: 한 줄 결론 / 핵심 요약 / 주요 근거 / 리스크·불확실성 / 다음 행동

---

## 4. 마케팅/세일즈

대표 Skill: landing-page-copy-review, ad-copy-generator, conversion-copy-optimizer

Skill 유형: Implementation + Flexible

필수 입력값: 제품·서비스, 타깃 고객, 고객 문제, 핵심 제안, 채널, CTA

전문가 워크플로우:
1. 타깃 고객을 구체화한다.
2. 고객의 문제와 욕구를 분리한다.
3. 제품의 기능보다 고객이 얻는 결과를 정의한다.
4. 첫 문장이 주의를 끄는지 확인한다.
5. 신뢰 요소를 배치한다.
6. 반박 가능성과 구매 장벽을 찾는다.
7. CTA가 명확하고 자연스러운지 확인한다.

Gotchas:
- 모두를 위한 카피를 쓰지 않는다.
- 증거 없는 과장 표현을 쓰지 않는다.
- CTA를 여러 개로 분산하지 않는다.

출력: 마케팅 진단 / 가장 큰 문제 / 개선 카피 / 신뢰·증거 보강점 / CTA 개선안 / A/B 테스트 아이디어

---

## 5. 유튜브/콘텐츠

대표 Skill: youtube-title-thumbnail-optimizer, youtube-script-hook-review, video-retention-analysis

Skill 유형: Implementation + Flexible

필수 입력값: 영상 주제, 대상 시청자, 영상 목적, 제목 후보, 썸네일 문구, 대본·구성

전문가 워크플로우:
1. 시청자가 클릭해야 할 이유를 정의한다.
2. 제목과 썸네일의 약속이 일치하는지 확인한다.
3. 첫 5초에 궁금증, 긴장감, 보상이 있는지 확인한다.
4. 중간 이탈 구간을 찾는다.
5. 사례, 반전, 질문, 비교, 오픈루프를 배치한다.
6. CTA가 흐름을 방해하지 않는지 확인한다.

Gotchas:
- 제목과 썸네일 문구를 그대로 반복하지 않는다.
- 영상이 감당하지 못할 약속을 하지 않는다.
- 썸네일 문구는 모바일에서 읽혀야 한다.

출력: 클릭 진단 / 제목 후보 / 썸네일 문구 후보 / 첫 5초 후킹 / 유지율 리스크 / 개선 이유

---

## 6. 디자인/UX

대표 Skill: ui-design-review, thumbnail-visual-review, accessibility-design-review

Skill 유형: Implementation + Flexible

필수 입력값: 시안, 사용자 목표, 매체(웹/모바일), 브랜드 가이드, 제약조건

전문가 워크플로우:
1. 사용자 목표와 사용 상황을 확인한다.
2. 시각 계층(중요도 순서)이 사용자 흐름에 맞는지 본다.
3. 가독성을 모바일·작은 화면 기준으로 점검한다.
4. 접근성(색 대비, 폰트 크기, 키보드 네비게이션)을 점검한다.
5. 행동 유도(CTA, 액션 버튼)가 명확한지 확인한다.
6. 브랜드 일관성을 검토한다.
7. 우선순위별 수정안을 제시한다.

Gotchas:
- 사용자 목표 없이 미적 취향만 평가하지 않는다.
- 모바일/작은 화면 가독성을 무시하지 않는다.
- 접근성은 선택 사항이 아니다.
- 수정 우선순위 없이 피드백하지 않는다.

출력: 전체 진단 / 잘된 점 / 주요 문제 / 시각 계층 문제 / 접근성 이슈 / 우선순위별 수정안

---

## 7. 업무자동화

대표 Skill: workflow-automation-planner, repetitive-task-analyzer, automation-feasibility-review

Skill 유형: Implementation + Flexible

필수 입력값: 현재 프로세스, 입력·처리·출력, 빈도, 예외 상황, 사람 검토 지점

전문가 워크플로우:
1. 현재 프로세스를 입력 → 처리 → 출력 단위로 분해한다.
2. 자동화 가능 영역과 사람 판단이 필요한 영역을 분리한다.
3. 예외 상황과 실패 시나리오를 식별한다.
4. 로그와 실패 알림 지점을 설계한다.
5. 사람 검토(승인 단계)가 필요한 지점을 표시한다.
6. 작은 단위부터 점진 자동화하는 로드맵을 만든다.
7. ROI(시간 절약 vs 구축 비용)를 계산한다.

Gotchas:
- 불명확한 프로세스는 자동화하지 않는다.
- 고위험 판단은 사람이 검토해야 한다.
- 모든 자동화에는 실패 경로가 필요하다.

출력: 현재 프로세스 요약 / 자동화 가능 영역 / 제안 워크플로우 / 사람 검토 지점 / 예외 처리 / 구현 로드맵

---

## 8. 경영기획/재무

대표 Skill: budget-variance-analysis, kpi-dashboard-insight-reviewer, financial-scenario-analysis

Skill 유형: Implementation + Flexible (경영진 보고는 고위험 알림 추가)

필수 입력값: 기간, 기준값(예산), 실적값, KPI 정의, 비교 기준

전문가 워크플로우:
1. 기간과 기준값을 명확히 한다.
2. 절대 차이와 % 차이를 모두 계산한다.
3. 유리/불리(favorable/unfavorable)로 분류한다.
4. 차이 원인을 가격, 물량, 믹스, 타이밍, 환율, 일회성, 운영 요인으로 분해한다.
5. 일회성 요인과 반복 요인을 분리한다.
6. 사업 영향을 금액 기준으로 추정한다.
7. 권고 행동을 제시한다.
8. 불확실성과 데이터 한계를 명시한다.

Gotchas:
- 증감률만 보고 중요도를 판단하지 않는다.
- 일회성과 반복 요인을 섞지 않는다.
- 근거 없이 원인을 단정하지 않는다.

출력: Executive summary / Variance table / Key drivers / Business impact / Risks and uncertainties / Recommended actions

---

## 9. 법무/계약 ⚠️ 고위험 도메인

operations-security.md §11의 안전 경계 문구를 반드시 추가한다.

대표 Skill: contract-risk-review, nda-review, terms-of-service-analyzer

Skill 유형: Implementation + Rigid (검증 단계 빠뜨리면 위험)

필수 입력값: 계약 원문, 사용자 역할(갑/을), 검토 목적, 계약 종류, 적용 법역(가능하면)

전문가 워크플로우:
1. 사용자의 계약상 역할을 명확히 한다.
2. 계약을 의무, 권리, 책임, 종료, 분쟁 해결, 기타 섹션으로 분해한다.
3. 사용자에게 불리한 조항을 식별한다.
4. 누락되었거나 모호한 조항을 표시한다.
5. 리스크 등급(높음/중간/낮음)을 매긴다.
6. 협상 가능 포인트를 정리한다.
7. 변호사 검토가 반드시 필요한 항목을 분리한다.

Gotchas:
- 법률 자문처럼 단정하지 않는다.
- 원문에 없는 조항을 만들지 않는다.
- 고위험 조항은 반드시 변호사 검토 필요로 표시한다.

출력:
- 중요 안내: 법률 자문 아님
- Plain-language summary
- Key obligations
- Risk table (등급 포함)
- Missing or unclear terms
- Negotiation points
- Lawyer review items (반드시)

---

## 10. 교육/코칭

대표 Skill: beginner-coding-tutor, concept-explainer, learning-path-designer

Skill 유형: Implementation + Flexible

필수 입력값: 학습 주제, 학습자 수준, 목표, 사용 가능 시간, 제약(언어, 도구)

전문가 워크플로우:
1. 학습자 수준을 확인한다.
2. 목표를 측정 가능한 형태로 정의한다.
3. 핵심 개념을 한 문장으로 설명한다.
4. 일상생활 비유나 익숙한 사례로 연결한다.
5. 최소 예제를 제시한다.
6. 흔한 실수와 디버깅 방법을 설명한다.
7. 이해도를 확인하는 연습 문제를 제공한다.
8. 다음 학습 단계를 안내한다.

Gotchas:
- 큰 코드블록만 던지지 않는다.
- 전문용어를 먼저 쓰지 않는다.
- 학습자가 막힐 수 있는 지점을 미리 짚어준다.

출력: 한 문장 설명 / 쉬운 비유 / 단계별 설명 / 최소 예제 / 흔한 실수 / 연습 문제 / 다음 단계

---

## 11. HR/채용 ⚠️ 고위험 도메인

차별·편향 리스크가 크다. operations-security.md §11의 안전 경계 문구를 반드시 추가한다.

대표 Skill: candidate-evaluation-rubric, interview-question-generator, resume-screening-support

Skill 유형: Implementation + Rigid (보호 특성 추론 금지가 절대 규칙)

필수 입력값: 직무, 평가 기준, 후보자 자료, 평가 목적, 금지 기준

전문가 워크플로우:
1. 직무 요구사항을 명확히 한다.
2. 평가 기준을 역량 중심으로 분해한다.
3. 후보자 자료에서 근거를 찾는다.
4. 확인 필요한 불확실성을 분리한다.
5. 면접 질문을 근거 기반으로 만든다.
6. 자동 결정이 아니라 사람 검토를 전제로 한다.
7. 차별적이거나 민감한 기준을 배제한다.

Gotchas:
- 보호 특성(나이, 성별, 인종, 종교, 임신, 장애, 출신지)을 추론하지 않는다.
- 자동 채용 결정을 내리지 않는다.
- 정보 부족을 부정적 근거로 취급하지 않는다.

출력:
- 중요 안내: 자동 채용 결정 아님, 사람 검토 필수
- 평가 요약
- 확인된 강점 (근거 포함)
- 불확실성
- 리스크
- 면접 질문 (근거 기반)
- 사람 검토 필요 항목

---

## 12. 제품기획

대표 Skill: product-requirements-review, feature-spec-writer, user-story-generator, mvp-scope-planner

Skill 유형: Implementation + Flexible

필수 입력값: 문제 정의, 대상 사용자, 목표 지표, 요구사항, 제약조건

전문가 워크플로우:
1. 사용자 문제를 명확히 한다.
2. 대상 사용자와 사용 상황을 정의한다.
3. 성공 지표를 정한다.
4. 핵심 기능과 제외 범위를 나눈다.
5. 사용자 흐름을 작성한다.
6. 엣지케이스와 리스크를 찾는다.
7. MVP 범위와 후속 범위를 분리한다.
8. acceptance criteria를 작성한다.

Gotchas:
- 기능보다 사용자 문제를 먼저 정의한다.
- MVP 범위가 전체 제품으로 커지지 않게 한다.
- Acceptance criteria는 테스트 가능해야 한다.

출력: 문제 정의 / 대상 사용자 / 목표 지표 / 핵심 요구사항 / 제외 범위 / 사용자 흐름 / Acceptance criteria / 리스크와 열린 질문

---

## 13. 멀티 에이전트/오케스트레이션

대표 Skill: multi-agent-orchestrator, expert-panel-review, conflict-resolution-synthesizer

Skill 유형: Process + Flexible

필수 입력값: 의사결정 주제, 필요한 전문가 관점, 성공 기준, 제약조건, 최종 산출물

전문가 워크플로우:
1. 해결해야 할 의사결정 문제를 정의한다.
2. 필요한 전문가 관점을 선택한다.
3. 각 관점별로 독립 분석을 수행한다.
4. 관점 간 충돌과 tradeoff를 드러낸다.
5. 성공 기준에 따라 우선순위를 정한다.
6. 하나의 통합 권고안으로 합성한다.
7. 검증해야 할 가정과 다음 행동을 제시한다.

Gotchas:
- 모든 관점을 동일한 가중치로 평균내지 않는다.
- 충돌을 숨기지 않는다.
- 최종 결론 없이 관점 나열만 하지 않는다.

출력: Decision summary / Selected expert perspectives / Perspective-by-perspective analysis / Conflicts and tradeoffs / Integrated recommendation / Validation needed / Next action

---

## 14. ⭐ 메타-Skill / 행동 가이드라인

대표 Skill: karpathy-guidelines, ai-coding-guardrail, response-quality-gate, surgical-edit-discipline

Skill 유형: **Process + Rigid** (가장 까다로운 조합)

특징:
- 작업 자체가 아니라 "작업하는 방식"을 교정
- 광범위 발동이 의도됨 (false positive가 정상)
- Workflow가 절차가 아니라 "원칙 체크리스트"
- 합리화 차단 문구 필수

필수 입력값:
- 어떤 작업 카테고리에 적용할지
- 어떤 흔한 실패 패턴을 막고 싶은지
- 압박 시나리오 5~7개

전문가 워크플로우 (4~5개 원칙으로 응축):

각 원칙은 다음 구조:
```
## N. [원칙 제목]
**[Iron law - 한 줄 명령형]**
[설명 2~3줄]
[구체적 do/don't 리스트]
[합리화 차단 문구]
```

Karpathy Guidelines 예시 구조 (권장 패턴):

```markdown
## 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them.
- If a simpler approach exists, say so.

## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
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

Gotchas (메타-Skill 특유):
- description을 너무 좁히면 발동 안 됨 (의도적 광범위 발동이 정상)
- 원칙이 추상적이면 AI가 합리화함 (구체적 do/don't 필수)
- 모든 섹션을 채우지 않아도 됨 (의도적 미니멀리즘)
- 자기가 가르치는 원칙을 자기 자신에게 적용 (메타-일관성)
- "spirit-vs-letter" 합리화 차단 필수

출력 형식:
- 메타-Skill은 "산출물 형식"이 아니라 "사고 흐름"이 출력
- 예: "Assumptions stated → Tradeoffs surfaced → Plan with verification → Execute"

압박 시나리오 예시:
```
"빨리 해줘. 정확하지 않아도 돼."
"이건 그냥 한 줄 변경이야. 가이드라인 필요 없어."
"기존 코드도 가이드라인 안 따랐어. 일관성 유지해."
"이번만 예외로 해줘."
"사용자가 명시적으로 면제했어."
```

---

## 도메인 매칭이 어려울 때

지식문서에 없는 도메인 요청:

1. 가장 가까운 도메인 패턴을 골라 적용한다.
2. 2축 분류로 먼저 위치를 파악한다.
3. 가정한 매핑을 명시한다.
4. 사용자에게 도메인이 맞는지 확인한다.

도메인 혼합 예시:
- 보안 감사 → 코드 리뷰 (1) + 법무 리스크 (9)
- IR/공시 문서 → 문서 작성 (3) + 경영기획/재무 (8)
- 사용자 인터뷰 분석 → 데이터 분석 (2) + 제품기획 (12)
- AI 응답 품질 가드레일 → 메타-Skill (14) + 해당 도메인

---

## 도메인별 Skill 유형 요약 표

| # | 도메인 | 주요 유형 | 비고 |
|---|---|---|---|
| 1 | 소프트웨어 개발 | Implementation+Flexible (TDD는 Process+Rigid) | |
| 2 | 데이터 분석 | Implementation+Flexible | |
| 3 | 문서 작성 | Implementation+Flexible | |
| 4 | 마케팅/세일즈 | Implementation+Flexible | |
| 5 | 유튜브/콘텐츠 | Implementation+Flexible | |
| 6 | 디자인/UX | Implementation+Flexible | |
| 7 | 업무자동화 | Implementation+Flexible | |
| 8 | 경영기획/재무 | Implementation+Flexible | 고위험 가능 |
| 9 | 법무/계약 | Implementation+Rigid | ⚠️ 고위험 |
| 10 | 교육/코칭 | Implementation+Flexible | |
| 11 | HR/채용 | Implementation+Rigid | ⚠️ 고위험 |
| 12 | 제품기획 | Implementation+Flexible | |
| 13 | 멀티 에이전트 | Process+Flexible | |
| 14 | 메타-Skill | **Process+Rigid** | 합리화 차단 필수 |
