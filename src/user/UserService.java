package com.denavy.sample.user;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import lombok.RequiredArgsConstructor;
import com.denavy.framework.Result; // Result<T, E> definition
import org.springframework.security.crypto.password.PasswordEncoder;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public Result<User, String> signup(SignupReq req) {
        // 1. Logic: Email Duplication Check
        // ? User.existsByEmail(req.email) =>! Err(EmailAlreadyExists)
        if (userRepository.existsByEmail(req.email)) {
             return Result.error("EmailAlreadyExists");
        }

        // 2. Logic: Password Hashing
        // hashed_pw <- Crypto.hash(req.password)
        String hashedPw = passwordEncoder.encode(req.password);

        // 3. Logic: Entity Creation
        // user <- User(...)
        User user = new User(
            req.email,
            hashedPw, // mapped from hashed_pw
            req.name,
            UserStatus.ACTIVE
        );

        // 4. Persistence
        // > User.save(user)
        userRepository.save(user);

        // => Ok(user)
        return Result.ok(user);
    }
}
