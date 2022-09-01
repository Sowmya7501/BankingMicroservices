package com.banking.userservice.service;

import com.banking.userservice.dto.UserRequest;
import com.banking.userservice.dto.UserResponse;
import com.banking.userservice.model.User;
import com.banking.userservice.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {

    private final UserRepository userRepository;

    public void createUser(UserRequest userRequest) {
        User user = User.builder()
                .name(userRequest.getName())
                .status(userRequest.getStatus())
                .balance(userRequest.getBalance())
                .build();

        userRepository.save(user);
        log.info("User {} is saved", user.getId());
    }

    public List<UserResponse> getAllUsers() {
        List<User> users = userRepository.findAll();

        return users.stream().map(this::mapToUserResponse).toList();
    }

    private UserResponse mapToUserResponse(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .name(user.getName())
                .status(user.getStatus())
                .balance(user.getBalance())
                .build();
    }
}