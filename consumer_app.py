from kafka import KafkaConsumer
import json

# Create the consumer
consumer = KafkaConsumer(
    "transactions",                              # topic name
    bootstrap_servers="localhost:9092",          # kafka broker
    auto_offset_reset="earliest",                # read from beginning
    enable_auto_commit=True,
    group_id="consumer-group-1",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("⚡ Waiting for messages...\n")

# Read messages continuously
for message in consumer:
    print("Received:", message.value)
