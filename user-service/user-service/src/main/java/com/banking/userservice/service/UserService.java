package com.banking.userservice.service;

import com.banking.userservice.dto.UserRequest;
import com.banking.userservice.dto.UserResponse;
import com.banking.userservice.model.User;
import com.banking.userservice.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;
import java.util.*;

@Service
@RequiredArgsConstructor
@Slf4j
public class UserService {

    private final UserRepository userRepository;
    private final WebClient.Builder webClientBuilder;

    public void createUser(UserRequest userRequest) {
        User user = User.builder()
                //.id(userRequest.getId())
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

    public UserResponse getUserbyId(Long id) {
        User user = userRepository.findById(id).orElse(null);

        return mapToUserResponse(user);
    }

    public Double getBalance(Long id) {
        User user = userRepository.findById(id).orElse(null);
        Double balance = webClientBuilder.build().get()
                .uri("http://localhost:8082/api/account/cb",
                        uriBuilder -> uriBuilder.queryParam("id",id).build())
                .retrieve()
                .bodyToMono(Double.class)
                .block();
        return balance;
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