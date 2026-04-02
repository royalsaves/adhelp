# Identity Management Portal (Refactoring Record)

해당 콘솔은 재직 중 임직원들의 빈번한 패스워드 변경 요청, 계정 초기화 요청, VPN QR 재생성 요청을 줄이기 위해 만들었던 사내 계정 지원 도구다.  
자주 들어오는 문의는 셀프서비스 형태로 처리하고, 예외적인 요청이나 추가 확인이 필요한 건은 Slack으로 기록을 남기도록 해서 SRE/DevOps 쪽 반복 작업 부담을 줄이는 데 목적이 있었다.

## 1. Problem Statement

### High Coupling

기존 Flask 엔드포인트 내부에 아래 요소가 한 파일에 섞여 있었다.

- HTTP 요청 처리
- AWS SDK 호출
- LDAP 비밀번호 검증
- 이메일 발송
- 알림 전송
- 보조 업무 자동화

이 구조에서는 단위 테스트가 어렵고, 특정 인프라를 교체할 때 영향 범위를 예측하기 어려웠다.

### Security Exposure

업무 도메인과 내부 운영 흐름이 코드 전반에 드러나 있었다.  
공개 저장소로 옮기려면 회사명, 내부 URL, 인증 흐름을 분리할 필요가 있었다.

### Environment Dependency

원래 구조는 실제 인프라 연결 없이는 로컬 실행 자체가 어려웠다.  
이 상태로는 포트폴리오 용도나 독립적인 검증 환경을 만들기 힘들었다.

## 2. Engineering Decisions

### Architecture: Hexagonal

핵심 로직과 인프라 코드를 분리하기 위해 Ports-and-Adapters 패턴을 적용했다.

- `domain/`: 모델과 포트 정의
- `application/`: 유스케이스 조합
- `adapters/`: AWS, LDAP, 메일, 알림, AI, 저장소 구현
- `api.py`: HTTP 엔트리포인트

의존 방향은 아래처럼 정리했다.

```text
frontend -> flask api -> application service -> domain port -> adapter
```

서비스 레이어는 외부 SDK를 직접 알지 않고 포트만 참조한다.  
실제 구현 교체는 adapter 레이어에서 처리한다.

### Runtime Separation

`APP_MODE` 기준으로 demo / live 모드를 분리했다.

- `demo`: 메모리 저장소, 콘솔 기반 side effect, 고정 AI 응답
- `live`: 실제 외부 연동 adapter 사용

같은 유스케이스를 유지하면서 실행 환경만 바꾸는 구조를 목표로 했다.

### Container-first Workflow

로컬 환경을 지저분하게 만들지 않도록 컨테이너 우선 실행 방식으로 정리했다.

- frontend는 Node stage에서 빌드
- runtime 이미지는 Python만 포함
- Flask가 빌드된 정적 파일을 함께 서빙

## 3. Implementation

### Directory Structure

```text
.
├── backend/
│   ├── app.py
│   └── ad_console/
│       ├── api.py
│       ├── app.py
│       ├── config.py
│       ├── domain/
│       ├── application/
│       └── adapters/
├── frontend/
│   └── src/
├── Dockerfile
└── docker-compose.yml
```

### Backend Notes

- 계정 신청, 비밀번호 변경/초기화, 잠금 해제 요청 흐름은 `application/services.py`에 위치
- Flask 라우팅과 응답 형식은 `api.py`에서 처리
- 디렉터리, 메일, 알림, 자동화, AI 응답은 adapter로 분리

### Frontend Notes

프런트는 흐름 검증용으로 유지했다.  
과한 기능 추가 대신 주요 API를 직접 눌러볼 수 있는 최소 UI만 남겼다.

## 4. Local Run

컨테이너 실행 기준:

```bash
docker compose up --build
```

접속 주소:

```text
http://127.0.0.1:5001
```

로컬 Python 실행도 가능하지만 기본 전제는 컨테이너 실행이다.

## 5. Operational Considerations

### Secrets

- `.env`는 커밋하지 않음
- 공개 저장소에는 `.env.example`만 유지

### Public Repository Sanitization

- 내부 도메인 제거
- 회사 식별자 일반화
- 운영 절차 문구 축소
- 실제 자격 증명 없이도 동작 가능한 demo 모드 유지

### Extensibility

아래 변경은 서비스 레이어 수정 없이 adapter 교체 수준에서 대응 가능하도록 정리했다.

- 다른 알림 채널 추가
- 다른 인증/디렉터리 연동 추가
- 저장소를 RDB로 교체
- 관리자 인증 계층 추가

## 6. Remaining Work

- 메모리 저장소를 영속 저장소로 교체
- 서비스 레이어 테스트 추가
- 관리자 승인 UI 보강
- 운영 로그 / 감사 이력 정리
- 개발 서버 대신 운영용 실행 구성을 별도 분리
