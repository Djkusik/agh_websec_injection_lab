# Task 2

## Run locally

If You don't want to use Docker Compose, You are able to run it individually with one of two methods:  
1. Using Docker with Dockerfile
```sh
docker build -t task2 .
docker run -p 5001:5001 task2
```
2. Using raw run
```sh
# Install Go language https://golang.org/doc/install
go get github.com/joho/godotenv
go build
./epilepsy
# epilepsy.exe if Windows
```
