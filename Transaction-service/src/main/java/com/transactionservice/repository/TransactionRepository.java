package com.transactionservice.repository;


import com.transactionservice.model.Transaction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;


public interface TransactionRepository extends JpaRepository<Transaction, Long> {
    public final static String GET_TRANSACTIONS = "SELECT * FROM t_transactions WHERE receiver_account = ?1 OR sender_account = ?1";

    @Query(value = GET_TRANSACTIONS, nativeQuery = true)
    List<Transaction> findBySender_accountOrReceiver_account(Long account);
}
