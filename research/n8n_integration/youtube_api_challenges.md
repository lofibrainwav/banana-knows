# n8n YouTube API 통합 주요 도전 과제 및 해결 방안

## 발견된 주요 문제점
1. **OAuth 리다이렉트 URL 문제**
   - 로컬호스트 URL 제한 (localhost:5678/rest/oauth2-credential/callback)
   - Google Cloud Console의 제한된 리다이렉트 URL 설정

2. **환경 변수 및 설정 도전**
   - `N8N_RUNNERS_ENABLED=true` 설정 필요
   - 포트 충돌 및 동적 포트 할당
   - 설정 파일 권한 조정

3. **YouTube 노드 업로드 오류**
   - 바이너리 데이터 모드 문제
   - 내부 오류 메시지
   - 비디오 처리 지연

## 권장 해결 방안
1. **OAuth 설정**
   - Google Cloud Console에서 정확한 리다이렉트 URL 구성
   - 외부 사용자 테스트 계정 추가
   - YouTube Data API v3 활성화

2. **환경 변수 최적화**
   ```bash
   export N8N_RUNNERS_ENABLED=true
   export N8N_DEFAULT_BINARY_DATA_MODE=filesystem
   export N8N_YOUTUBE_API_KEY=YOUR_API_KEY
   ```

3. **포트 및 프로세스 관리**
   ```bash
   # 충돌 포트 프로세스 종료
   lsof -i :5678 | grep LISTEN | awk '{print $2}' | xargs kill -9
   lsof -i :5679 | grep LISTEN | awk '{print $2}' | xargs kill -9
   ```

4. **설정 파일 권한 조정**
   ```bash
   chmod 600 /Users/bbookpro/.n8n/config
   export N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
   ```

## 추가 고려 사항
- n8n 버전 최신화 (현재 1.88.0)
- 디버깅 모드 활성화 (`N8N_VERBOSE=true`)
- 워크플로 내보내기 및 가져오기 테스트

## 다음 단계
1. OAuth 인증 재검토
2. 환경 변수 최적화
3. YouTube API 연동 세부 설정 확인
4. 워크플로 안정성 테스트 