package com.corebankingservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;

@SpringBootApplication
@EnableEurekaClient
public class CoreBankingServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(CoreBankingServiceApplication.class, args);
	}

}
