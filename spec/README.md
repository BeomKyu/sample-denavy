# /spec — 운영 명세 계층 (Operational Specification Layer)

이 디렉토리는 Denavy 3계층 아키텍처의 **논리 계층**입니다.

## 역할
- `/dna`의 제약 조건을 바탕으로 **비즈니스 로직과 제어 흐름**을 정의합니다.
- 조건 분기, 할당, 반복 등을 **기호 논리학(TOON DSL)**으로 표현합니다.
- 자연어는 오직 주석(`#`)으로만 허용합니다.

## 파일 규칙
- 확장자: `.spec`
- 경로는 `/dna` 및 `/src` 계층과 **1:1 대칭**을 이루어야 합니다.

```
예시:
  /dna/auth/login.dna   ↔   /spec/auth/login.spec   ↔   /src/auth/login.py
```

## TOON 기호 체계

| 기호   | 의미                                      |
|--------|-------------------------------------------|
| `!`    | Invariant — 필수 제약 검증, 위반 시 Halt  |
| `?`    | Decision — 조건 분기 (IF)                 |
| `>`    | Execute — 상태 변이, 함수/API 호출        |
| `<-`   | Assign — 변수 할당 및 상태 매핑           |
| `*`    | Loop — 배열 및 컬렉션 반복               |
| `=>`   | Return — 정상 결과 반환                   |
| `!=>!` | Error — 에러 전파 (Result 모나드 패턴)    |
| `@`    | Import & Metadata — 외부 모듈 참조        |
| `<:`   | Inherit — 상위 레지스트리 규칙 상속       |
| `$`    | Semantic Anchor — 글로벌 심볼 참조        |

## TOON 작성 예시

```
@import $User from ~dna/auth/login.dna

# 로그인 플로우
login(email, password)
  ! email != null && password != null
  result <- > db.find(User, email)
  ? result == null
    !=>! Err(UserNotFound)
  ? > hash.verify(password, result.password) == false
    !=>! Err(InvalidCredentials)
  token <- > jwt.sign(result.id, result.role)
  => token
```
