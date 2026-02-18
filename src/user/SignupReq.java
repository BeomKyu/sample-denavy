package com.denavy.sample.user;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record SignupReq(
    @NotBlank
    String email,

    @NotBlank
    @Size(min = 8, max = 32)
    String password,

    @NotBlank
    String name
) {}
