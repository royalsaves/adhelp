# Reading Order

이 저장소는 아래 순서로 보는 편이 빠르다.

## 1. README

- 프로젝트를 왜 정리했는지
- 어떤 문제를 해결했는지
- 실행 방식이 무엇인지

## 2. ARCHITECTURE

- 레이어 분리 이유
- 포트와 adapter 책임
- demo / live 분리 기준

## 3. application/services.py

- 실제 유스케이스 중심 파일
- 계정/비밀번호/잠금 해제 흐름 확인 가능

## 4. adapters/

- 외부 의존성 구현 위치
- runtime별 교체 지점 확인 가능

## 참고 포인트

이 프로젝트는 기능 시연보다 아래 항목을 보여주는 쪽에 가깝다.

- 운영성 강한 Flask 코드 정리
- 인프라 의존성 분리
- 공개 저장소 전환을 위한 sanitization
- 컨테이너 우선 실행 흐름 정리
