# 회원가입 비즈니스 로직 흐름 명세
@import SignupInput     from ~dna/user/signup.dna
@import User            from ~dna/user/entity.dna
@import $SecurityPolicy from ~dna/root.dna

signup(input: SignupInput)
  # ── 이메일 중복 검증 ─────────────────────────────────────────────────────
  ? > db.exists(User, email == input.email)
    !=>! Err(EmailAlreadyExists)

  # ── 유저네임 중복 검증 ───────────────────────────────────────────────────
  ? > db.exists(User, username == input.username)
    !=>! Err(UsernameAlreadyExists)

  # ── 비밀번호 일치 확인 ───────────────────────────────────────────────────
  ? input.password != input.password_confirm
    !=>! Err(PasswordMismatch)

  # ── 비밀번호 해싱 ────────────────────────────────────────────────────────
  hashed_pw <- > hash.bcrypt(input.password, $SecurityPolicy.password_hash)

  # ── 사용자 엔티티 생성 및 DB 저장 ───────────────────────────────────────
  > db.create(User,
      username        : input.username
      email           : input.email
      hashed_password : hashed_pw
      full_name       : input.full_name
    )

  # ── 정상 반환 ────────────────────────────────────────────────────────────
  => Ok
