# n8n YouTube API 통합 문제 해결 분석

## 주요 문제점
1. 포트 충돌 (5678, 5679)
2. 플래그 오류 (--apiKey, --port)
3. 설정 파일 권한 문제
4. Deprecation Warning

## 해결 전략
- 포트 동적 할당 (5680)
- 환경 변수 활용
  - N8N_RUNNERS_ENABLED=true
  - N8N_YOUTUBE_API_KEY 설정
- 설정 파일 권한 조정 (chmod 600)

## 테스트 결과
- 워크플로 내보내기 시도: 실패
- 추가 조사 필요

## 다음 단계
1. 워크플로 내보내기 실패 원인 분석
2. n8n 설정 재검토
3. YouTube API 연동 세부 설정 확인 