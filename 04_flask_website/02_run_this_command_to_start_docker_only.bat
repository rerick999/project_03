docker build --tag python-docker .
docker run -p 8080:8080 -P python-docker
pause