# Architecture Notes

## 목적

이 문서는 현재 코드가 왜 이런 구조를 가지는지 정리한 메모다.  
핵심은 기능 소개가 아니라 결합도 제어와 실행 환경 분리다.

## 배경

초기 상태에서는 Flask 엔드포인트가 아래 역할을 동시에 수행했다.

- 요청 파싱
- 유효성 검사
- 외부 디렉터리 호출
- 비밀번호 검증
- 이메일 발송
- 알림 발송
- 보조 자동화 호출

이 구조에서는 테스트, 교체, 공개 저장소 전환이 모두 불리했다.

## 구조

```text
HTTP / UI
  -> API
  -> Application
  -> Domain Port
  -> Adapter
```

### API

위치:

- `backend/ad_console/api.py`

역할:

- 요청/응답 처리
- 상태 코드 결정
- 서비스 호출 진입점 유지

여기서는 비즈니스 로직을 처리하지 않는다.

### Application

위치:

- `backend/ad_console/application/services.py`

역할:

- 계정 신청
- 계정 승인/거부
- 비밀번호 변경
- 인증 코드 발송
- 비밀번호 초기화
- 잠금 해제 요청

유스케이스 조합만 담당하고 외부 SDK에는 직접 의존하지 않는다.

### Domain

위치:

- `backend/ad_console/domain/models.py`
- `backend/ad_console/domain/ports.py`

역할:

- 시스템 데이터 구조 정의
- 외부 기능에 대한 포트 정의

서비스 레이어는 이 포트를 기준으로만 동작한다.

### Adapters

위치:

- `backend/ad_console/adapters/`

역할:

- 실제 외부 연동 구현
- demo / live 모드별 구현 분리

주요 adapter:

- directory
- emailing
- notifications
- automation
- ai
- repositories

## Runtime Modes

### demo

- 메모리 저장소 사용
- 외부 연동 대신 로그 출력
- AI도 고정 응답 사용

목적은 로컬 실행과 공개 저장소 검증이다.

### live

- 실제 외부 연동 adapter 사용
- 같은 서비스 레이어 유지

목적은 런타임 교체 시 영향 범위를 adapter 레이어로 한정하는 것이다.

## DevOps Notes

실행은 컨테이너 기준으로 맞췄다.

- frontend: Node stage build
- runtime: Python slim image
- 최종 컨테이너에서 Flask가 정적 파일 서빙

이 방식으로 로컬 `npm install` 없이 전체 앱을 띄울 수 있다.

## 정리

이 구조의 목적은 세 가지다.

1. 서비스 레이어에서 인프라 의존성 제거
2. demo / live 환경 분리
3. 공개 저장소 전환 시 민감한 맥락 제거 용이성 확보
