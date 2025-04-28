# 종합 연구 요약: 유튜브 자동 분석·제작 파이프라인

## 1. 프로젝트 개요
- **목표:** 유튜브 영상 트랜스크립트 추출 → LLM 분석 → 메모리뱅크 저장 → 최종 콘텐츠(프로그램·앱·음악·아트·영상) 자동 제작
- **핵심 스택:** `youtube-transcript-api`, WhisperX/faster-whisper, n8n, LangFlow, OpenAI Function Calling, Vector DB(ChromaDB/FAISS)
- **주요 요구사항:** 100% 커버리지, WER ≤ 10%, 응답 지연 < 200ms, 파일 크기 제한(18KB)

## 2. 파이프라인 단계 및 연구 결과

### Stage 0: Debug & Monitoring
- **구성:** Structured Logging(JSON), Health Check Endpoint, Slack/Webhook 알림, 대시보드/UI
- **연구:** Prometheus/Sentry 연동 방안, JSON 로그 스키마, 경보·재시도 정책

### Stage 1: Ingestion (트랜스크립트)
- **기술:** youtube-transcript-api + Webshare Proxy, WhisperX/faster-whisper(Fallback), ASR 성능 벤치마크
- **연구:** Proxy 통합 모듈 구조, WER·Latency·리소스·비용 비교, 하이브리드 파이프라인 설계

### Stage 2: Analysis (LLM 병렬)
- **기술:** 한국어→영어 번역, Async 큐 기반 LLM 호출, Obsidian HTML/Markdown 렌더러
- **연구:** Obsidian·Msty 워크플로우, Dataview·Templater 프로토타입, Vault 자동화 스크립트

### Stage 3: Storage (메모리뱅크)
- **기술:** DB 스키마(MySQL/SQLite), CRUD API, Embedding 연동(ChromaDB/FAISS), 검색·캐시 모듈
- **연구:** 메타데이터·컨텍스트 모델링, Redis vs Postgres Chat Memory 비교

### Stage 4: Creative Build
- **기술:** 최종 산출물 스토리보드, 초안 생성(LLM·Memory Bank), 피드백 루프, 자동 배포
- **연구:** 스토리보딩 자동화, 리뷰 UI 설계, GitHub Actions·n8n 워크플로우 활용

### Stage 5: Dynamic Tool Orchestration & Meta-Cognition
- **기술:** Tool Registry, LLM Orchestrator Interface, On-Demand 설치, Async/큐 실행, 피드백 루프
- **연구:** n8n vs LangFlow 비교(노코드 vs 로우코드), Function Calling 적용, 메타인지 컨텍스트 저장소 설계

## 3. 주요 도구·통합 연구

### n8n
- 400+ 커넥터, LangChain 내장, MPI Client/Server 지원, RAG·메모리·병렬 처리, UI 디버깅

### LangFlow
- LangChain 컴포넌트 시각 조합, JSON Flow 내보내기, 라이브 디버깅, 커스텀 플러그인 개발

### Function Calling
- 함수 메타데이터(`functions`): 이름·설명·파라미터 스키마 정의
- 오케스트레이션: LLM이 `tool_calls` 반환 → Orchestrator가 실제 함수 실행 → 결과 주입
- 모범 사례: 명확한 설명, 단일 책임, 오류 처리, 출력 검증, 파인튜닝 데이터셋

## 4. 종합 권장 전략
1. **빠른 검증 → 배치 처리 → 커스텀 플러그인** 3단계 반복 개선 사이클 적용
2. 기능별 함수 레지스트리 구축 및 Orchestrator 모듈화
3. Fine-Tuning으로 Function Calling 정확도 극대화
4. Async 큐 기반 모니터링·재시도 정책 통합
5. Obsidian Vault 연동 프로토타입 → n8n 워크플로우 전환

## 5. 다음 단계
- `research/overall_research_summary.md` 검토 및 피드백
- 함수 레지스트리 스키마, Orchestrator 설계 문서화
- 주요 Stage별 PoC(Proof of Concept) 개발·벤치마크
- 파인튜닝용 Function Calling 데이터셋 수집 및 실험

## 6. '소스놀이터' 영상 심층 인사이트 [YouTube]
- **AI 코딩 환경:** Claude Desktop과 Vibe Coding 플러그인을 활용해 VSCode 유사 UX에서 실시간 코드 스니펫 생성 및 테스트
- **mcp.json 기반 도구 관리:** 단일 설정 파일로 `terminal`, `filesystem`, `googleSearch`, `selenium` 서버 호출 메타데이터 정의 → 동적 로딩
- **프로젝트 스캐폴딩 워크플로:** `npm init obsidian-plugin`, `pipenv`/`poetry` 환경 생성 → AI 기반 스크립트 자동 생성(`npx ai-gen-script`) → 즉시 실행 및 결과 주석 삽입
- **코드·대화 연동:** Vibe Coding 노트 작성 후 MCP 터미널 자동 실행 → 결과를 Obsidian Vault(analysis/)에 HTML·MD로 동기화
- **자동 파일 분할·배포:** `wc -c` 자동 체크 → 18KB 초과 시 `split -b 18k`로 분할, analysis 디렉토리 체계적 관리 → 배포 `npx deploy-pipeline`
- **테스트·디버깅 체계:** 실행 전 사용자 확인 룰(#15, #16) → 예외 발생 시 Sentry 연동 알림 → UI 내 Node별 재실행·Replay 지원
- **다단계 승인 프로세스:** 각 스크립트 단계별 승인 및 검토 → 파이프라인 무결성 보장
- **파이프라인 적합성:** 위 워크플로는 Stage 1~5 모든 단계에서 빠른 PoC→MVP→스케일아웃 사이클에 최적화됨 