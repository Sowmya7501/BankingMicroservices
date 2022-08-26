package com.corebankingservice.service;

import com.corebankingservice.repository.AccountRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class AccountService {
    @Autowired
    private final AccountRepository accountRepository;

    @Transactional
    public boolean checkBalance(String accountNumber){

        return accountRepository.findByAccountNumber(accountNumber).getAccount;

    }
}
