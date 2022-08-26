package com.corebankingservice.controller;

import com.corebankingservice.service.AccountService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/account")
@RequiredArgsConstructor
public class AccountController {
    @Autowired
    private final AccountService accountService;

    @GetMapping("/{accountNumber}")
    @ResponseStatus(HttpStatus.OK)
    public AccountResponse checkBalance(@PathVariable("accountNumber") String accountNumber){
        return accountService.checkBalance(accountNumber);
    }
}
