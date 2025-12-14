📌 Real-Time Fraud Detection System

Kafka + Streamlit + Machine Learning (Random Forest)

This project implements a Real-Time Fraud Detection System that identifies suspicious financial transactions using a trained Random Forest Machine Learning model, real-time Kafka streaming, and a Streamlit dashboard for visualization.

🚀 Features

✔ Real-time streaming using Apache Kafka
✔ Kafka Producer & Consumer architecture
✔ Machine Learning model (Random Forest)
✔ Automated Feature Engineering
✔ Fraud Probability (Risk Score)
✔ Instant Fraud Alerts on Streamlit Dashboard
✔ Dynamic Metrics & Live Transaction Table
✔ Plotly charts for visualization
✔ Production-ready code structure

🏗️ System Architecture
+----------------+       +----------------+        +--------------------+
|  Data Generator| ----> |  Kafka Producer| -----> |   Kafka Topic      |
+----------------+       +----------------+        +--------------------+
                                                                 |
                                                                 v
                                                          +--------------+
                                                          | Kafka Consumer|
                                                          +--------------+
                                                                 |
                                                                 v
                                                      +--------------------+
                                                      | ML Model (RF)      |
                                                      +--------------------+
                                                                 |
                                                                 v
                                                      +--------------------+
                                                      | Streamlit Dashboard|
                                                      +--------------------+

📁 Project Structure
Real_time_fraud_detection/
│
├── consumer_app.py
├── kafka_app.py
├── realtime_fraud_detection.py
├── ui_dashboard.py
│
├── create_historical_data.py
├── feature_engineering.py
├── train_model.py
│
├── fraud_model.pkl
├── historical_transactions.csv
│
└── README.md

🧠 Machine Learning Model

Algorithm: Random Forest Classifier

Type: Binary Classification (Fraud / Normal)

Metrics: Accuracy, Risk Score

Dataset: Synthetic + Historical transaction data

Model File: fraud_model.pkl

🧩 Feature Engineering Includes:

Transaction Hour

Day of Week

Country Encoding

High Amount Flag

Avg Spending Pattern

Amount Difference from User Average

Timestamp Processing

📊 Real-Time Dashboard

The dashboard displays:

⭐ Total Transactions

🚨 Fraud Cases

✔️ Normal Cases

📄 Latest Transaction Data

🔥 Fraud Alerts (with Risk Score)

📈 Plotly Charts

Example alert:

⚠ FRAUD DETECTED — Risk Score: 0.76

🛠️ How to Run the Project
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Start Zookeeper
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

3️⃣ Start Kafka Broker
.\bin\windows\kafka-server-start.bat .\config\server.properties

4️⃣ Create Kafka Topic
.\bin\windows\kafka-topics.bat --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

5️⃣ Run Kafka Producer
python kafka_app.py

6️⃣ Run Fraud Detection Consumer
python realtime_fraud_detection.py

7️⃣ Run Streamlit Dashboard
streamlit run ui_dashboard.py


Dashboard URL:

http://localhost:8501

📦 Requirements
streamlit
pandas
numpy
scikit-learn
kafka-python
plotly
joblib
