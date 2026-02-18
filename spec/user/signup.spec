# FILE: sample-denavy/spec/user/signup.spec

import dna/user/user.dna (User, UserStatus)

struct SignupReq
    email: str
    password: str @len(8..32)
    name: str

fn signup(req: SignupReq) -> Result<User, Error>
    # 1. Logic: Email Duplication Check
    # (DNA checks regex format, Spec checks business rule uniqueness)
    ? User.existsByEmail(req.email) =>! Err(EmailAlreadyExists)

    # 2. Logic: Password Hashing
    # (DNA defines 'pwd_hash' field, Spec defines HOW to generate it)
    hashed_pw <- Crypto.hash(req.password)

    # 3. Logic: Entity Creation
    user <- User(
        email: req.email,
        pwd_hash: hashed_pw,
        name: req.name,
        status: UserStatus.Active
    )

    # 4. Persistence
    > User.save(user)
    => Ok(user)
