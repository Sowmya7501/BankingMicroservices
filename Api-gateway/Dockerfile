FROM openjdk:17
EXPOSE 8089
ADD target/api-gateway-docker.jar api-gateway-docker.jar
ENTRYPOINT ["java","-jar","/api-gateway-docker.jar"]