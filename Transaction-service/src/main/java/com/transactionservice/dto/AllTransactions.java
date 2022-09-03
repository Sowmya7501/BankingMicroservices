package com.transactionservice.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class AllTransactions {
    private Long transaction_id;
    private String transaction_number;
    private Long sender_account;
    private Long receiver_account;
    private Double amount;
}
