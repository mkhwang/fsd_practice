import os
import json

from kafka import KafkaProducer


class KafkaService:
    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=os.getenv("BOOTSTRAP_SERVERS", "localhost:9092"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def send(self, topic: str, message: dict):
        self.kafka_producer.send(topic, message)
