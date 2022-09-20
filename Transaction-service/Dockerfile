FROM openjdk:17
EXPOSE 8081
ADD target/transaction-service-docker.jar transaction-service-docker.jar
ENTRYPOINT ["java","-jar","/transaction-service-docker.jar"]