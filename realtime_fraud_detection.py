from kafka import KafkaConsumer
import json, joblib
import pandas as pd
from feature_engineering import engineer_features

# Load trained model
model = joblib.load("fraud_model.pkl")

# Kafka consumer
consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("🔍 Real-time fraud detection started...\n")

for msg in consumer:
    tx = msg.value

    # Convert to DataFrame
    df = pd.DataFrame([tx])

    # Feature engineering
    features = engineer_features(df)

    # Make prediction
    prediction = model.predict(features)[0]

    if prediction == 1:
        print("🚨 FRAUD DETECTED:", tx)
    else:
        print("✔ Normal Transaction:", tx)
