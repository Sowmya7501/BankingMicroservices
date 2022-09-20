FROM openjdk:17
EXPOSE 8088
ADD target/user-service-docker.jar user-service-docker.jar
ENTRYPOINT ["java","-jar","/user-service-docker.jar"]