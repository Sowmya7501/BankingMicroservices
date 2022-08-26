package com.transactionservice.model;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;

@Entity
@Table(name="t_transactions")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Transaction {
    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)

    private Long transaction_id;
    private String transaction_number;
    private Long sender_account;
    private Long receiver_account;
    private Double amount;

}
