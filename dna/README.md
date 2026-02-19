# /dna — 데이터 및 제약 계층 (Data & Constraints Layer)

이 디렉토리는 Denavy 3계층 아키텍처의 **기반 계층**입니다.

## 역할
- 데이터의 뼈대(Entity)와 타입을 정의합니다.
- 절대 변하지 않는 **정적 보안/비즈니스 제약 조건(Policy)**만 선언합니다.
- **로직이나 제어 흐름은 포함될 수 없습니다.**

## 파일 규칙
- 확장자: `.dna`
- 경로는 `/spec` 및 `/src` 계층과 **1:1 대칭**을 이루어야 합니다.

```
예시:
  /dna/auth/login.dna   ↔   /spec/auth/login.spec   ↔   /src/auth/login.py
```

## TOON 작성 예시

```
# Entity: User
User
  id       : UUID  ! required
  email    : Str   ! @format(email) @unique
  password : Str   ! @len(8,72) @hashed
  role     : Enum[admin, user, guest]
```

> **주의:** 자연어는 오직 주석(`#`)으로만 허용합니다.
