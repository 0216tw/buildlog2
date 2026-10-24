# BuildLog 개발 환경 기준

## 1. 문서 목적

이 문서는 Phase 0에서 확정한 개발 환경, 패키지 버전, 주소, 환경 변수와 이후 사용할 명령을 기록합니다.

Phase 0에서는 패키지를 설치하거나 애플리케이션 코드를 만들지 않았습니다. 아래 설치·실행 명령은 이후 Phase에서 사용할 기준입니다.

## 2. 현재 PC 확인 결과

확인 날짜: 2026-10-24

| 항목 | 확인 결과 | 상태 |
| --- | --- | --- |
| 운영체제 | Windows, PowerShell | 사용 가능 |
| Python | 3.12.7 | 사용 가능 |
| pip | 24.2 | 사용 가능 |
| Python 내장 SQLite | 3.45.3 | 테스트 DB로 사용 가능 |
| Node.js | 24.13.0 | 사용 가능 |
| npm | 11.6.2 | `npm.cmd`로 사용 가능 |
| npx | 11.6.2 | `npx.cmd`로 사용 가능 |
| FastAPI·React 패키지 | 설치되지 않음 | Phase 1·2에서 설치 |

PowerShell 실행 정책 때문에 `npm.ps1`은 실행되지 않습니다. 시스템 정책은 변경하지 않고 `npm.cmd`와 `npx.cmd`를 사용합니다.

## 3. 선택한 안정 버전

### 백엔드

| 패키지 | 버전 | 역할 |
| --- | --- | --- |
| Python | 3.12.7 | 백엔드 실행 언어 |
| FastAPI | 0.162.0 | API 서버 |
| Uvicorn | 0.54.0 | 개발용 ASGI 서버 |
| SQLAlchemy | 2.1.6 | 데이터 모델과 조회 |
| Alembic | 1.20.1 | 데이터베이스 구조 변경 이력 |
| pydantic-settings | 2.16.1 | 환경 변수 설정 |
| psycopg | 3.3.6 | Supabase PostgreSQL 연결 |
| pytest | 9.1.1 | 백엔드 자동 테스트 |
| HTTPX | 0.28.1 | FastAPI API 테스트 |
| pwdlib | 0.3.1 | 비밀번호 해시 처리 |
| PyJWT | 2.15.1 | 로그인 토큰 처리 |
| email-validator | 2.3.0 | 이메일 형식 검사 |

### 프론트엔드

| 패키지 | 버전 | 역할 |
| --- | --- | --- |
| Node.js | 24.13.0 | 프론트엔드 실행 환경 |
| React | 19.3.1 | 사용자 화면 |
| React DOM | 19.3.1 | 브라우저 화면 출력 |
| TypeScript | 7.0.2 | 타입이 있는 프론트엔드 코드 |
| Vite | 8.3.5 | 개발 서버와 빌드 |
| Vite React 플러그인 | 6.1.2 | React와 Vite 연결 |
| React Router DOM | 7.18.4 | 화면 이동 |
| Vitest | 5.0.5 | 프론트엔드 테스트 실행 |
| React Testing Library | 16.3.3 | 사용자 행동 중심 화면 테스트 |
| create-vite | 9.3.1 | React 프로젝트 생성 |
| React 타입 | 19.3.0 | React TypeScript 타입 정보 |
| React DOM 타입 | 19.3.0 | React DOM TypeScript 타입 정보 |
| jsdom | 29.0.1 | 브라우저 화면 테스트 환경 |

선택한 패키지는 2026-10-24 기준 공식 PyPI와 npm 레지스트리의 안정 배포 버전입니다. 설치 시 의존성 충돌이 확인되면 버전을 임의로 바꾸지 않고 문서의 버전과 변경 이유를 함께 갱신합니다.

## 4. 개발 주소

| 용도 | 주소 |
| --- | --- |
| React 개발 화면 | `http://localhost:5173` |
| FastAPI 개발 서버 | `http://127.0.0.1:8000` |
| API 기본 주소 | `http://127.0.0.1:8000/api` |
| FastAPI API 문서 | `http://127.0.0.1:8000/docs` |
| 상태 확인 API | `http://127.0.0.1:8000/api/health` |

React 개발 주소만 FastAPI의 허용 출처에 등록합니다.

## 5. 환경 변수

### 백엔드 `backend/.env`

| 이름 | 용도 | 실제 값 관리 |
| --- | --- | --- |
| `DATABASE_URL` | FastAPI가 사용할 Supabase Session pooler 접속 문자열 | 사용자가 Supabase Dashboard에서 복사해 로컬에 입력 |
| `MIGRATION_DATABASE_URL` | Alembic 구조 변경에 사용할 Supabase 직접 접속 문자열 | 사용자가 Supabase Dashboard에서 복사해 로컬에 입력 |
| `TEST_DATABASE_URL` | SQLite 테스트 DB | 안전한 예시값을 `.env.example`에 기록 가능 |
| `APP_SECRET_KEY` | 로그인 정보 보호 | 개발 시작 시 로컬에서 임의 생성 |
| `FRONTEND_ORIGIN` | FastAPI 호출을 허용할 React 주소 | `http://localhost:5173` |

권장 테스트 값은 `sqlite+pysqlite:///./database/test.sqlite3`입니다. 자동 테스트에서는 테스트 전용 파일을 초기화하며 Supabase 데이터를 사용하지 않습니다.

### 프론트엔드 `frontend/.env`

| 이름 | 용도 | 값 |
| --- | --- | --- |
| `VITE_API_BASE_URL` | React가 호출할 FastAPI 기본 주소 | `http://127.0.0.1:8000/api` |

프론트엔드 환경 변수에는 Supabase 접속 문자열, 데이터베이스 비밀번호, 앱 비밀 키를 넣지 않습니다.

## 6. Supabase 연결 기준

- FastAPI는 장시간 실행되는 백엔드이므로 `DATABASE_URL`에는 Supabase Dashboard의 `Connect` 메뉴에서 복사한 Session pooler 연결 문자열을 사용합니다.
- 데이터베이스 비밀번호의 예약 문자는 연결 문자열에서 URL 인코딩해야 합니다.
- 연결 문자열에는 SSL을 요구하는 설정을 적용합니다.
- Alembic 구조 변경에는 `MIGRATION_DATABASE_URL`을 사용합니다.
- 직접 연결이 현재 네트워크의 IPv6 조건 때문에 동작하지 않으면 값을 임의로 바꾸지 않고 Supabase가 제공하는 연결 방식 중 마이그레이션에 사용할 수 있는 방식을 다시 확인합니다.
- React는 Supabase에 직접 연결하지 않습니다.
- Supabase Auth는 첫 버전에 사용하지 않습니다.

## 7. 이후 Phase에서 사용할 명령 기준

아래 명령은 아직 실행하지 않았습니다.

### 백엔드

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install "fastapi==0.162.0" "uvicorn[standard]==0.54.0" "sqlalchemy==2.1.6" "alembic==1.20.1" "pydantic-settings==2.16.1" "psycopg[binary]==3.3.6" "pytest==9.1.1" "httpx==0.28.1" "pwdlib[argon2]==0.3.1" "PyJWT==2.15.1" "email-validator==2.3.0"
backend/.venv/Scripts/python.exe -m pytest backend/tests
backend/.venv/Scripts/python.exe -m uvicorn app.main:app --reload --app-dir backend
```

### 프론트엔드

```powershell
npx.cmd create-vite@9.3.1 frontend --template react-ts
npm.cmd --prefix frontend install
npm.cmd --prefix frontend install --save-exact react@19.3.1 react-dom@19.3.1 react-router-dom@7.18.4
npm.cmd --prefix frontend install --save-dev --save-exact typescript@7.0.2 vite@8.3.5 @vitejs/plugin-react@6.1.2 vitest@5.0.5 @testing-library/react@16.3.3 @types/react@19.3.0 @types/react-dom@19.3.0 jsdom@29.0.1
npm.cmd --prefix frontend run dev
npm.cmd --prefix frontend run test
npm.cmd --prefix frontend run build
```

실제 Phase에서는 정확한 패키지와 명령을 파일 구조에 맞게 실행하고 결과를 다시 확인합니다.

## 8. 사용자가 준비할 내용

Phase 0과 Phase 1·2에는 사용자가 제공할 비밀값이 없습니다.

Phase 3을 시작하기 전에는 다음이 필요합니다.

1. Supabase 프로젝트를 생성합니다.
2. Supabase Dashboard의 `Connect` 메뉴에서 Session pooler 연결 문자열을 확인합니다.
3. 마이그레이션용 직접 연결 문자열을 확인합니다.
4. 실제 문자열과 데이터베이스 비밀번호는 채팅이나 문서에 보내지 않고 `backend/.env`에 직접 입력합니다.

Phase 12에서 Safari 확인을 하려면 Mac, iPhone, iPad 또는 원격 브라우저 환경이 필요할 수 있습니다.

## 9. Phase 0 완료 확인

- [x] 문서의 기술 구성을 FastAPI·React·Supabase·SQLite 테스트로 통일했습니다.
- [x] Python, SQLite, Node.js, npm 실행 가능 여부를 확인했습니다.
- [x] 사용할 안정 패키지 버전을 기록했습니다.
- [x] 프론트엔드·백엔드 개발 주소를 정했습니다.
- [x] 환경 변수 이름과 비밀값 관리 위치를 정했습니다.
- [x] Supabase와 SQLite의 역할을 구분했습니다.
- [x] 이후 사용할 실행·테스트 명령 형식을 정했습니다.
- [x] 패키지 설치와 애플리케이션 코드 작성을 하지 않았습니다.

## 10. Phase 1 완료 확인

확인 날짜: 2026-10-24

- [x] `backend/.venv`에 Python 가상환경을 만들었습니다.
- [x] 문서에서 정한 버전으로 백엔드 패키지를 설치했습니다.
- [x] 설치할 패키지 버전을 `backend/requirements.txt`에 기록했습니다.
- [x] FastAPI 애플리케이션과 공통 설정·API 폴더를 만들었습니다.
- [x] `GET /api/health` 상태 확인 API를 만들었습니다.
- [x] React 개발 주소 `http://localhost:5173`만 허용하는 CORS 기본 설정을 적용했습니다.
- [x] SQLite 연결과 상태 API를 확인하는 자동 테스트를 작성했습니다.
- [x] 자동 테스트 2개와 패키지 충돌 검사를 통과했습니다.
- [x] 실제 서버에서 상태 API, API 문서, OpenAPI 문서가 열리는 것을 확인했습니다.
- [x] Supabase 비밀값 없이 모든 Phase 1 확인을 완료했습니다.
