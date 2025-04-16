import datetime
import json

from dotenv import load_dotenv
from fastapi import FastAPI

from transactions import TransactionMaker
from utils import RedisService

load_dotenv()

app = FastAPI()

tx_maker = TransactionMaker()
redis_service = RedisService()


@app.get("/generate/transaction")
async def generate_tx():
    tx_maker.generate_event()
    return {"success": True}


@app.get("/fraud/candidate")
async def get_fraud_candidate():
    keys = redis_service.keys(
        f'fraud:candidate:{datetime.datetime.today().strftime("%Y-%m-%d")}:*'
    )
    return [json.loads(redis_service.get(k)) for k in keys]


@app.get("/fraud/confirmed")
async def get_fraud_confirmed():
    keys = redis_service.keys(
        f'fraud:confirmed:{datetime.datetime.today().strftime("%Y-%m-%d")}:*'
    )
    return [json.loads(redis_service.get(k)) for k in keys]
