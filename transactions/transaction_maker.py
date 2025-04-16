import dataclasses
import os
import random
import time
from typing import List
from uuid import uuid4

import dotenv
from faker import Faker

from transactions import Transaction
from utils import KafkaService


class TransactionMaker:
    def __init__(self):
        dotenv.load_dotenv()
        self.user_count = int(os.getenv("TRANSACTION_USER_COUNT", 100))
        self.event_count = int(os.getenv("TRANSACTION_EVENT_COUNT", 1000))
        self.event_interval = int(os.getenv("TRANSACTION_EVENT_INTERVAL", 100)) * 0.001
        self.fake = Faker()
        self.producer = KafkaService()
        self.transaction_topic = os.getenv("TRANSACTION_TOPIC", "transaction-events")

    def generate_event(self):
        print(
            f"Generating {self.event_count} transactions with an interval of {self.event_interval} ms"
        )
        fake_transactions: List[Transaction] = self.generate_fake_transaction(
            self.user_count, self.event_count
        )

        for tx in fake_transactions:
            self.producer.send(self.transaction_topic, dataclasses.asdict(tx))
            time.sleep(self.event_interval)

        print("Finished generating transactions")

    def generate_fake_users(self, num_users: int) -> list:
        users = []
        for idx in range(num_users):
            user_name = self.fake.name()
            users.append(
                {
                    "id": idx,
                    "name": user_name,
                }
            )
        return users

    def generate_fake_transaction(
        self, user_count: int, transaction_count: int
    ) -> List[Transaction]:
        result = []

        users = self.generate_fake_users(user_count)

        standard_time = int(time.time()) - (3600 * 24)

        for idx in range(transaction_count):
            sender, receiver = random.sample(users, 2)

            standard_time += random.randint(1, 100)

            transaction = Transaction(
                id=str(uuid4()),
                sender_id=sender["id"],
                sender_name=sender["name"],
                amount=random.randint(100, 10000) * 100,
                timestamp=standard_time,
                ip=self.fake.ipv4(),
                receiver_id=receiver["id"],
                receiver_name=receiver["name"],
            )
            result.append(transaction)

        return result
