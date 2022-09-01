package com.banking.userservice.model;

import lombok.*;
import org.springframework.data.annotation.Id;
import javax.persistence.*;
import org.hibernate.annotations.DynamicInsert;
import org.hibernate.annotations.DynamicUpdate;


import java.math.BigDecimal;



@Entity
@DynamicInsert
@DynamicUpdate
@Table(name="t_account")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String status;          //description
    private BigDecimal balance;     //price
}