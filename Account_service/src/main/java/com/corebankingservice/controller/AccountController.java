package com.corebankingservice.controller;

import com.corebankingservice.dto.TransactionRequest;
import com.corebankingservice.service.AccountService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/account")
@RequiredArgsConstructor
public class AccountController {

    private final AccountService accountService;

    @PostMapping("/trans")
    @ResponseStatus(HttpStatus.OK)
    public boolean checkBalance(@RequestBody TransactionRequest transactionRequest){

        return accountService.checkBalance(transactionRequest);
    }
    /*
    @GetMapping("/cb")
    @ResponseStatus(HttpStatus.OK)
    public Double getBalance(@RequestParam Long id) {
        return accountService.getBalance(id);
    }

     */
}
