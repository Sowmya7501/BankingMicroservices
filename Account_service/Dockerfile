FROM openjdk:17
EXPOSE 8082
ADD target/banking-service-docker.jar banking-service-docker.jar
ENTRYPOINT ["java","-jar","/banking-service-docker.jar"]