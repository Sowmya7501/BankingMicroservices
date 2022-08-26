FROM openjdk:17
EXPOSE 8761
ADD target/discovery-service-docker.jar discovery-service-docker.jar
ENTRYPOINT ["java","-jar","/discovery-service-docker.jar"]