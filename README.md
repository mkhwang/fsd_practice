# 이상거래 감지 Practice

## 프로젝트 목표
- rest api를 이용해 다수의 거래를 생성하여 kafka에 전송
- 실시간 거래 저장
  - spark streaming을 이용해 kafka에서 모든거래를 수신하여 hdfs에 저장
- data pipeline 구축
  - spark streaming을 이용한 이상거래 후보와 확정된 거래를 redis에 저장하여 fastapi로 제공

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

