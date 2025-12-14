
from kafka import KafkaProducer
import json
import time
import random

def get_producer():
    return KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

producer = get_producer()

while True:
    data = {
        "transaction_id": random.randint(1000, 9999),
        "amount": round(random.uniform(10, 2000), 2),
        "country": random.choice(["IN", "US", "UK", "JP"]),
        "user_id": random.randint(1, 50),
        "timestamp": time.time()
    }

    producer.send("transactions", data)
    print("Sent:", data)
    time.sleep(1)
