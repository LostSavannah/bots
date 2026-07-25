docker stop test-whatsapp-app
docker rm test-whatsapp-app
docker build -t test-whatsapp-app .
docker run -p 8080:8080 -it --name test-whatsapp-app test-whatsapp-app