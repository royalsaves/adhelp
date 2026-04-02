# Architecture Notes

## 1. 개요

이 문서는 현재 코드 구조와 레이어 분리 기준을 정리한 문서입니다. 목적은 기능 소개가 아니라 결합도 제어와 실행 환경 분리입니다.

## 2. 기존 구조의 문제

초기 상태에서는 Flask 엔드포인트가 아래 역할을 동시에 수행하고 있었습니다.

- 요청 파싱
- 유효성 검사
- 외부 디렉터리 호출
- 비밀번호 검증
- 이메일 발송
- 알림 발송
- 보조 자동화 호출

이 구조에서는 테스트, 교체, 공개 저장소 전환이 모두 불리합니다.

## 3. 현재 구조

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

유스케이스 조합만 담당하고 외부 SDK에는 직접 의존하지 않습니다.

### Domain

위치:

- `backend/ad_console/domain/models.py`
- `backend/ad_console/domain/ports.py`

역할:

- 시스템 데이터 구조 정의
- 외부 기능 포트 정의

### Adapters

위치:

- `backend/ad_console/adapters/`

역할:

- 실제 외부 연동 구현
- demo / live 모드별 구현 분리

주요 adapter는 아래와 같습니다.

- directory
- emailing
- notifications
- automation
- ai
- repositories

## 4. Runtime Mode

### demo

- 메모리 저장소 사용
- 외부 연동 대신 로그 출력
- AI도 고정 응답 사용

로컬 실행과 공개 저장소 검증을 위한 모드입니다.

### live

- 실제 외부 연동 adapter 사용
- 서비스 레이어는 동일하게 유지

실제 환경 연동을 위한 모드입니다.

## 5. 컨테이너 실행 방식

실행은 컨테이너 기준으로 맞췄습니다.

- frontend: Node stage build
- runtime: Python slim image
- 최종 컨테이너에서 Flask가 정적 파일 서빙

이 방식으로 로컬 `npm install` 없이 전체 앱을 실행할 수 있습니다.

## 6. 정리

현재 구조의 목적은 아래 세 가지입니다.

1. 서비스 레이어에서 인프라 의존성 제거
2. demo / live 환경 분리
3. 공개 저장소 전환 시 민감한 맥락 제거 용이성 확보
