# 이상거래 감지 Practice

## 설치

```bash
brew install virtualenv
virtualenv --python=python3.11 .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
```

## docker-compose

```bash
docker-compose up -d 
```

```bash
docker-compose down -V
```

## HDFS Permission
```bash
docker exec -it namenode hdfs dfs -mkdir -p /warehouse/transactions
docker exec -it namenode hdfs dfs -chown {run_user}:supergroup /warehouse
docker exec -it namenode hdfs dfs -chown {run_user}:supergroup /warehouse/transactions
```

## fastapi RUN

```bash
. .venv/bin/activate
uvicorn fastapi_main:app --reload
```

## fastapi doc
- http://localhost:8000/docs

#### generate transaction

```http request
GET http://localhost:8000/generate_transaction
```

#### get fraud candidate & confirmed

```http request
GET http://localhost:8000/fraud/candidate
```

```http request
GET http://localhost:8000/fraud/confirmed
```

