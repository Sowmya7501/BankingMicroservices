package com.transactionservice.controller;

import com.transactionservice.dto.AllTransactions;
import com.transactionservice.dto.TransactionRequest;
import com.transactionservice.model.Transaction;
import com.transactionservice.service.TransactionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/transaction")
@RequiredArgsConstructor
public class TransactionController {

    private final TransactionService transactionService;


    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public String completeTransaction(@RequestBody TransactionRequest transactionRequest) {
        return transactionService.completeTransaction(transactionRequest);

    }
    @GetMapping(value="/{accountnumber}")
    @ResponseStatus(HttpStatus.OK)
    public List<AllTransactions> getTransaction(@PathVariable("accountnumber") Long accountNumber){
        return transactionService.getTransactions(accountNumber);
    }
}
