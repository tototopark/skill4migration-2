with open("f:/pe/public_html/test-migration/skill-builder/skills/code-migration-quality-gate/SKILL.md", "r", encoding="utf-8") as f:
    content = f.read()

# Replace step names
content = content.replace("### 3단계. Gate 1:", "### 4단계. Gate 1:")
content = content.replace("### 4단계. 모듈 단위 격리", "### 5단계. 모듈 단위 격리")
content = content.replace("### 5단계. Gate 2: 1:1 회귀 대조", "### 6단계. Gate 2: 1:1 회귀 대조")
content = content.replace("### 6단계. 격차 보고서 및 통합", "### 7단계. 격차 보고서 및 통합")
content = content.replace("- [ ] **Gate 1 완료**", "- [ ] **Gate 1 완료 (4단계 계획 표 작성)**")
content = content.replace("- [ ] **Gate 2 통과**", "- [ ] **Gate 2 통과 (6단계 회귀 대조)**")

with open("f:/pe/public_html/test-migration/skill-builder/skills/code-migration-quality-gate/SKILL.md", "w", encoding="utf-8") as f:
    f.write(content)

print("SKILL.md reindexed successfully.")
