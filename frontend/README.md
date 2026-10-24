# BuildLog 프론트엔드

React와 TypeScript로 만든 BuildLog 화면입니다. 데이터는 FastAPI API를 통해서만 읽고 저장합니다.

## 실행

프로젝트 루트에서 다음 명령을 사용합니다.

```powershell
npm.cmd --prefix frontend install
npm.cmd --prefix frontend run dev
```

개발 화면은 `http://localhost:5173`에서 열립니다.

## 확인

```powershell
npm.cmd --prefix frontend run test
npm.cmd --prefix frontend run lint
npm.cmd --prefix frontend run build
```

API 기본 주소는 `frontend/.env`의 `VITE_API_BASE_URL`로 바꿀 수 있습니다. 실제 비밀값은 프론트엔드 환경 변수에 넣지 않습니다.
