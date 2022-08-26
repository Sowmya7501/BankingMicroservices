package com.transactionservice.service;


import com.transactionservice.dto.TransactionRequest;
import com.transactionservice.model.Transaction;
import com.transactionservice.repository.TransactionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.UUID;


@Service
@RequiredArgsConstructor
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final WebClient.Builder webClientBuilder;
    public String completeTransaction(TransactionRequest transactionRequest){
        Transaction transaction = new Transaction();
        /*System.out.println(transactionRequest.getAmount());
        System.out.println(transactionRequest.getReceiver_account());
        System.out.println(transactionRequest.getSender_account());*/
        transaction.setTransaction_number(UUID.randomUUID().toString());
        transaction.setSender_account(transactionRequest.getSender_account());
        transaction.setReceiver_account(transactionRequest.getReceiver_account());
        transaction.setAmount(transactionRequest.getAmount());

        Boolean result = false;
        result = webClientBuilder.build().post()
                .uri("http://localhost:8082/api/account/trans")
                .bodyValue(transactionRequest)
                        .retrieve()
                                .bodyToMono(Boolean.class)
                                        .block();
        System.out.println(result);
        if(result){
            transactionRepository.save(transaction);
            return "Transaction Completed Successfully";
        }
        else{
            return "Not enough Balance";
        }

    }
}
