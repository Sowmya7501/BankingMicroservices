package com.banking.userservice.repository;

import com.banking.userservice.model.User;
import org.springframework.data.jpa.repository.JpaRepository;


public interface UserRepository extends JpaRepository<User, Long> {
}
