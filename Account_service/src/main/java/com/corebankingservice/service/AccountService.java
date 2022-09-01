package com.corebankingservice.service;

import com.corebankingservice.dto.TransactionRequest;
import com.corebankingservice.repository.AccountRepository;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.corebankingservice.model.Account;

import java.math.BigDecimal;

@Service
@RequiredArgsConstructor
public class AccountService {

    private final AccountRepository accountRepository;

    @Transactional
    @SneakyThrows
    public boolean checkBalance(TransactionRequest transactionRequest){
        boolean ans;
        System.out.println(transactionRequest.getSender_account());
        System.out.println(transactionRequest.getReceiver_account());
        System.out.println(transactionRequest.getAmount());
        Account account1 = accountRepository.findByAccountNumber(transactionRequest.getSender_account()).get();

        Account account2 = accountRepository.findByAccountNumber(transactionRequest.getReceiver_account()).get();
        Account sender_account = accountRepository.getById(account1.getId());
        Account receiver_account = accountRepository.getById(account2.getId());
        Double amount = transactionRequest.getAmount();
        Double senderBalance = sender_account.getAccountBalance();
        Double receiverBalance = receiver_account.getAccountBalance();
        if(amount <= senderBalance) {
            sender_account.setAccountBalance(senderBalance-amount);
            accountRepository.save(sender_account);
            Account saccount = accountRepository.getById(account1.getId());

            System.out.println(saccount.getAccountBalance());
            receiver_account.setAccountBalance(amount+receiverBalance);
            accountRepository.save(receiver_account);
            Account raccount = accountRepository.getById(account2.getId());
            System.out.println(raccount.getAccountBalance());
            ans=true;
        }
        else{
            ans=false;
        }
        return ans;
    }

    @Transactional(readOnly = true)
    public Double getBalance(Long id) {
        Account account = accountRepository.findById(id).orElse(null);
        return account.getAccountBalance();
    }
}
