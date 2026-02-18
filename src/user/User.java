package com.denavy.sample.user;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.UUID;
import java.time.LocalDateTime;
import org.hibernate.annotations.CreationTimestamp;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @NotBlank
    @Size(min = 2, max = 20)
    @Column(nullable = false)
    private String name;

    @NotBlank
    @Pattern(regexp = "^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$")
    @Column(nullable = false, unique = true)
    private String email;

    @NotBlank
    @JsonIgnore // @hidden
    @Column(nullable = false)
    private String pwdHash;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserStatus status = UserStatus.ACTIVE;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    // Constructors, Getters, Setters (Omitted for brevity, but implied)
    protected User() {}

    public User(String email, String pwdHash, String name, UserStatus status) {
        this.email = email;
        this.pwdHash = pwdHash;
        this.name = name;
        this.status = status;
    }

    // Getters...
    public UUID getId() { return id; }
    public String getEmail() { return email; }
    // ...
}
