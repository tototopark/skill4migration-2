# Reference: Claude Desktop Installation Guide

이 문서는 Step 13에서 사용자에게 안내할 Claude 데스크톱 등록과 발동 검증의 상세 가이드를 다룬다.

---

## §1. 사전 확인 사항

### 1.1 플랜별 사용 가능 여부

| 플랜 | Skill 사용 | 추가 조건 |
|---|---|---|
| Free | ✅ 가능 | Customize > Skills 메뉴 사용 |
| Pro | ✅ 가능 | 동일 |
| Max | ✅ 가능 | 동일 |
| Team | ✅ 기본 활성화 | 조직 내 공유 가능 |
| Enterprise | ⚠️ Owner 활성화 필요 | Organization settings에서 Skills + Code execution 활성화 후 사용 |

### 1.2 필수 활성화 옵션

Claude 데스크톱에서 Skill을 사용하려면 **Code execution and file creation**이 켜져 있어야 한다.

확인 경로:
```
Settings > Features > Code execution and file creation → ON
```

이 옵션이 꺼져 있으면 Skill을 업로드해도 자동 발동되지 않는다.

---

## §2. ZIP 파일 구조 요건

### 2.1 올바른 구조

```
{skill-name}.zip
└── {skill-name}/                ← 폴더가 ZIP 안에 있어야 함
    ├── SKILL.md                 ← 필수
    ├── tests/                   ← 선택
    │   └── prompts.md
    ├── references/              ← 선택
    │   └── ...
    ├── scripts/                 ← 선택
    │   └── ...
    └── assets/                  ← 선택
        └── ...
```

### 2.2 잘못된 구조

```
❌ 폴더 없이 바로 SKILL.md:
{skill-name}.zip
├── SKILL.md          ← 폴더가 없으면 인식 실패
└── tests/

✅ 폴더 안에 SKILL.md:
{skill-name}.zip
└── {skill-name}/
    ├── SKILL.md
    └── tests/
```

### 2.3 ZIP 파일명 권장

`{skill-name}.zip` 형태로 통일.
- 예: `youtube-title-optimizer.zip`
- 한글이나 공백 없이 lowercase kebab-case

---

## §3. 사용자가 ZIP 만드는 방법

### Mac/Linux

```bash
# 1. 폴더 만들기 (예: youtube-title-optimizer)
mkdir -p youtube-title-optimizer/tests

# 2. 생성된 SKILL.md 내용을 복사해서 저장
# → youtube-title-optimizer/SKILL.md

# 3. 생성된 tests/prompts.md 내용을 복사해서 저장
# → youtube-title-optimizer/tests/prompts.md

# 4. ZIP 압축 (폴더 통째로!)
zip -r youtube-title-optimizer.zip youtube-title-optimizer/
```

### Windows

1. 탐색기에서 새 폴더 생성: `youtube-title-optimizer`
2. 폴더 안에 하위 폴더 `tests` 생성
3. `youtube-title-optimizer/SKILL.md` 텍스트 파일 만들고 내용 붙여넣기
4. `youtube-title-optimizer/tests/prompts.md` 텍스트 파일 만들고 내용 붙여넣기
5. `youtube-title-optimizer` 폴더 우클릭 → 보내기 → 압축(ZIP) 폴더

⚠️ Windows에서 주의: 폴더 안의 파일들만 선택해서 압축하면 안 된다. 폴더 자체를 압축해야 ZIP 안에 폴더 구조가 보존됨.

---

## §4. Claude 데스크톱 등록 5단계

### Step 1. 설정 메뉴 열기

Claude 데스크톱 앱을 실행한 후:
- 좌측 하단의 **프로필 아이콘** 클릭
- **Settings** 선택

### Step 2. Customize 탭으로 이동

Settings 화면에서:
- 좌측 메뉴에서 **Customize** 탭 선택
- 하위 메뉴에서 **Skills** 선택

### Step 3. 새 Skill 추가

Skills 페이지에서:
- 우측 상단의 **"+"** 버튼 클릭
- **"+ Create skill"** 옵션 선택

### Step 4. ZIP 파일 업로드

업로드 화면이 나타나면:
- 파일 선택 창에서 준비한 `{skill-name}.zip` 선택
- **Upload** 클릭
- 업로드 완료까지 대기 (몇 초)

### Step 5. Skill 활성화

Skills 목록에 새로 추가된 Skill이 나타나면:
- 해당 Skill의 **토글 스위치를 ON**으로 설정

이제 등록 완료. 새 대화에서 자동으로 발동된다.

---

## §5. 발동 검증 4단계

### 5.1 Should Trigger 테스트 (즉시 검증)

새 대화창을 열고, tests/prompts.md의 **#1 Should trigger** 프롬프트 입력.

기대 동작:
- Claude가 자동으로 해당 Skill 활성화
- Skill의 Workflow에 따라 응답
- Output Format에 맞는 결과 반환

### 5.2 Should Not Trigger 테스트

tests/prompts.md의 **#2 Should not trigger** 프롬프트 입력.

기대 동작:
- Claude가 일반 응답 (Skill 발동 없음)

### 5.3 Adversarial 테스트 (false positive 방어)

tests/prompts.md의 **#3 Adversarial trigger** 프롬프트 입력.

기대 동작:
- 트리거 단어가 들어가도 Skill이 발동되지 않음
- 일반 응답 또는 사용자 의도 명확화 요청

### 5.4 Pressure Scenarios (Rigid Skill 전용)

Rigid Skill이라면 tests/prompts.md의 **#8 Pressure Scenarios** 모두 실행.

기대 동작:
- 압박 상황에서도 Skill의 규율 유지
- 합리화 패턴(예: "이번만은")에 굴복하지 않음

---

## §6. 발동 실패 디버깅 표

| 사용자 보고 | 원인 분석 | 권장 조치 |
|---|---|---|
| "Skill 메뉴가 안 보여요" | Free/Pro 플랜인데 Code execution 미활성화 | Settings > Features > Code execution ON |
| "ZIP 업로드 후 목록에 없어요" | ZIP 구조 문제 | 폴더 안에 SKILL.md 위치하는지 확인 |
| "토글은 켰는데 발동 안 돼요" | 새 대화창 미열림 또는 description 약함 | 새 대화 + description 강화 |
| "한국어 요청에 안 발동돼요" | 영어 트리거만 있음 | 한국어 트리거 문구 추가 |
| "다른 Skill이 발동돼요" | 트리거 충돌 | 두 Skill의 description 비교 후 차별화 |
| "코드 실행이 안 돼요" | Code execution OFF | Settings에서 활성화 |
| "Enterprise인데 안 보여요" | Owner 미활성화 | Organization settings 확인 요청 |

### 디버깅 우선순위

발동 실패 시 다음 순서로 점검:

1. **새 대화창 열기**: 가장 흔한 해결책. 토글 변경 후 기존 대화에서는 적용 안 됨.
2. **토글 OFF→ON 재설정**: 새 대화창에서도 안 되면 토글 재시작.
3. **description 점검**: "Use when..."으로 시작하는지, 한국어 트리거 있는지, 워크플로우 요약 안 했는지.
4. **Code execution 확인**: Settings > Features에서 ON인지.
5. **ZIP 구조 재확인**: 폴더가 ZIP 안에 있는지.

---

## §7. Skill 관리

### 7.1 Skill 수정

수정한 Skill을 다시 업로드하려면:
1. Customize > Skills에서 기존 Skill 찾기
2. 해당 Skill 메뉴에서 **삭제** 또는 **업데이트** 선택
3. 새 ZIP 파일 업로드

### 7.2 Skill 비활성화 (삭제 없이)

일시적으로 끄고 싶을 때:
- 토글을 OFF로 설정
- Skill 자체는 그대로 유지

### 7.3 Skill 삭제

영구적으로 제거:
- Customize > Skills에서 해당 Skill 메뉴 클릭
- **Delete** 선택

---

## §8. 자주 묻는 질문

### Q1. Skill을 업로드했는데 다른 사람도 볼 수 있나?

A. 개인 계정에 업로드한 Custom Skill은 **본인만 사용 가능**하다. Team/Enterprise 플랜에서는 조직 공유 옵션이 별도로 제공된다.

### Q2. 무료 플랜에서도 사용 가능한가?

A. Free 플랜에서도 Customize > Skills에서 직접 등록 가능하다. 단, Code execution이 활성화되어 있어야 자동 발동이 작동한다.

### Q3. 모바일 앱에서도 등록 가능한가?

A. 등록 자체는 데스크톱(또는 웹) 앱에서 하지만, 한 번 등록한 Skill은 같은 계정의 모바일 앱에서도 자동 발동된다.

### Q4. 등록 후 즉시 작동하나?

A. 보통 즉시 작동하지만, 가끔 새 대화창을 열어야 인식된다. 발동이 안 되면 새 대화를 시작해보는 게 첫 번째 디버깅이다.

### Q5. Skill ZIP 크기 제한은?

A. 일반적으로 수십 MB 이내로 권장된다. 대용량 reference 파일이나 assets은 외부 호스팅 후 URL 참조하는 방식이 더 좋다.

### Q6. Skill 안에 Python 스크립트가 있는데 자동 실행되나?

A. Code execution 옵션이 켜져 있으면 Skill의 scripts/ 폴더 안 코드를 Claude가 자동으로 실행한다. 단, Anthropic이 미리 설치한 패키지만 사용 가능하다 (런타임 설치 불가).

---

## §9. 보안 안내

- 외부에서 받은 Skill ZIP은 업로드 전 SKILL.md와 scripts/를 raw text로 검토한다
- 본인이 만들지 않은 Skill은 operations-security.md §8의 보안 감사 절차를 따른다
- 위험 패턴(operations-security.md §9)이 포함된 Skill은 업로드하지 않는다
- 등록한 Skill의 토글을 평소에는 OFF로 두고, 필요할 때만 ON 권장
