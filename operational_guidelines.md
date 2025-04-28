# Project Operational Guidelines

**Version:** 1.0
**Date:** 2024-08-04

## 1. Introduction

이 문서는 "바이브코딩 지식관리 시스템" 프로젝트의 안정적이고 효율적인 진행을 위해 모든 참여자(AI 어시스턴트 포함)가 준수해야 할 핵심 운영 규칙 및 가이드라인을 정의합니다. 특히, 버전 관리의 부재로 인해 발생한 문제를 해결하고 재발을 방지하기 위해 Git 워크플로우 준수를 강조합니다.

## 2. Git Workflow (Mandatory)

**모든 코드, 문서, 설정 변경 사항은 반드시 Git 버전 관리를 통해 추적되어야 합니다. 커밋되지 않은 로컬 작업물은 공식적인 프로젝트 진행 상태로 간주하지 않습니다.**

*   **Commit Frequency:** 의미 있는 최소 작업 단위가 완료될 때마다 즉시 `git add` 및 `git commit`을 수행합니다. 주요 기능 개발 전/후, 버그 수정 후, 설정 변경 후 등 변경이 발생하면 커밋합니다.
*   **Commit Messages:**
    *   변경 내용과 그 이유를 명확하고 간결하게 설명합니다.
    *   [Conventional Commits](https://www.conventionalcommits.org/) 형식 사용을 강력히 권장합니다. (예: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`)
    *   예시:
        ```bash
        feat(ingestion): Add initial script for fetching transcripts via API
        fix(api): Handle rate limit errors with exponential backoff
        docs(readme): Update setup instructions
        chore: Update .gitignore for macOS files
        ```
*   **Branching Strategy (Future):** 현재는 `main` 브랜치에 직접 커밋하지만, 향후 기능 개발 시에는 기능 브랜치(feature branch) 사용을 고려합니다.
*   **`.gitignore` Management:**
    *   프로젝트와 관련 없는 파일은 `.gitignore`에 명시하여 철저히 제외합니다.
    *   **필수 제외 대상:** `venv/`, `.venv/`, `node_modules/`, `__pycache__/`, `.pytest_cache/`, `.DS_Store`, `._*`, IDE 설정 파일 (`.idea/`, `.vscode/` 등), 민감 정보 파일 (API 키 파일 등 - 환경 변수 사용 권장).
    *   `.gitignore` 파일 자체도 버전 관리합니다.

## 3. Standard Work Cycle (Plan-Code-Commit-Update)

모든 작업은 다음 사이클을 따릅니다.

1.  **Plan:** `project_plan.md`에서 해당 작업 내용을 확인하고 필요시 목표 및 단계를 명확히 합니다.
2.  **Code:** 로컬 환경에서 코드 구현, 문서 작성, 설정 변경 등 실제 작업을 수행합니다.
3.  **Verify:** (최소한) 린터 실행, 간단한 로컬 테스트 등으로 기본적인 검증을 수행합니다.
4.  **Commit:** **완료된 작업 단위를 Git에 커밋합니다.** (규칙 2 준수)
5.  **Update Plan:** **커밋된 내용**을 바탕으로 `project_plan.md`의 해당 작업 상태를 업데이트하고, 관련 커밋 해시나 작업 내용을 간략히 로그로 남깁니다.

## 4. Code Quality & Testing

*   **Linting:** 커밋 전 `flake8` 등 설정된 린터를 통과해야 합니다. (`pre-commit` 훅 활용 권장)
*   **Testing:**
    *   새로운 기능이나 로직 추가 시 `pytest`를 사용한 단위 테스트 작성을 **강력히 권장**합니다.
    *   외부 API 연동 등 복잡한 부분은 통합 테스트를 고려합니다.
    *   테스트 코드는 `/tests` 디렉토리에 위치하며, Git으로 관리합니다.

## 5. Environment & Tools

*   **Working Directory:** 모든 작업은 `/Volumes/BRNESTRM/Claude_Project` 내에서 수행합니다.
*   **Directory Structure:** `research/` (리서치 문서), `analysis/` (분석 결과), `scripts/` (주요 실행 스크립트), `tests/` (테스트 코드) 등 정의된 디렉토리 구조를 유지합니다.
*   **MCP Tools:** 사용 가능한 MCP 도구(`terminal`, `web_search`, `edit_file` 등)를 적극 활용하여 생산성을 높입니다.
*   **Dependencies:** Python (`requirements.txt`, `pyproject.toml`), Node.js (`package.json`) 의존성은 명시적으로 관리하고 Git에 포함시킵니다.

## 6. Documentation & Research

*   **`project_plan.md`:** 항상 최신 상태를 유지하며, 작업 진행 상황은 **커밋 기반**으로 업데이트합니다.
*   **Research:** 충분한 사전 리서치(최소 20개 소스 등 기존 규칙 유지)를 수행하고, 결과는 `research/` 디렉토리에 마크다운 형식 등으로 체계적으로 정리하여 Git에 커밋합니다.
*   **Analysis:** 분석 결과물은 `analysis/` 디렉토리에 저장하고 Git에 커밋합니다.

## 7. File Size Management

*   기존 규칙대로, 18kb를 초과할 것으로 예상되는 파일은 사전에 분할 계획을 세우고 `split -b 18k` 등을 사용하여 관리합니다. 분할된 파일도 Git으로 관리합니다.

---

**이 가이드라인은 프로젝트의 안정성과 효율성을 위한 필수적인 약속입니다. 모든 과정에서 이 규칙들을 염두에 두고 작업을 진행해야 합니다.** 