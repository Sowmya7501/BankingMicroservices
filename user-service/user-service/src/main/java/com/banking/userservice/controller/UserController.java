package com.banking.userservice.controller;

import com.banking.userservice.dto.UserRequest;
import com.banking.userservice.dto.UserResponse;
import com.banking.userservice.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public void createUser(@RequestBody UserRequest userRequest) {
        userService.createUser(userRequest);
    }

    @GetMapping
    @ResponseStatus(HttpStatus.OK)
    public List<UserResponse> getAllUsers() {
        return userService.getAllUsers();
    }

    @GetMapping(value="/{id}")
    @ResponseStatus(HttpStatus.OK)
    public UserResponse getUserbyId(@PathVariable("id") Long id) {
        System.out.println("it came here?");
        return userService.getUserbyId(id); }

    @GetMapping(value="/cb/{id}")
    @ResponseStatus(HttpStatus.OK)
    public Double getBalance(@PathVariable("id") Long id) { return userService.getBalance(id);}
}