# Project Guide

## 1. 읽는 순서

이 저장소는 아래 순서로 보는 편이 빠릅니다.

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `backend/ad_console/application/services.py`
4. `backend/ad_console/adapters/`

## 2. 먼저 볼 내용

### README

- 프로젝트 배경
- 구조 변경 목적
- 실행 방식

### ARCHITECTURE

- 레이어 분리 이유
- 포트와 adapter 책임
- demo / live 분리 기준

## 3. 코드 기준으로 볼 파일

### `application/services.py`

- 실제 유스케이스 중심 파일
- 계정/비밀번호/잠금 해제 흐름 확인 가능

### `adapters/`

- 외부 의존성 구현 위치
- runtime별 교체 지점 확인 가능

## 4. 확인 포인트

이 저장소에서는 아래 항목을 중심으로 보면 됩니다.

- 운영성 강한 Flask 코드 정리
- 인프라 의존성 분리
- 공개 저장소 전환을 위한 sanitization
- 컨테이너 우선 실행 흐름 정리
