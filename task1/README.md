# Task 1

## Run locally

If You don't want to use Docker Compose, You are able to run it individually with one of two methods:  
1. Using Docker with Dockerfile
```sh
docker build -t task1 .
docker run -p 5000:5000 task1
```
2. Using raw run
```sh
pip3 install -U pip setuptools wheel
pip3 install -r requirements.txt
python3 -m spacy download en
python3 run.py
```