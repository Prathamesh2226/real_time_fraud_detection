import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from kafka import KafkaConsumer
import json
import joblib
import time
from feature_engineering import engineer_features

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Real-Time Fraud Detection",
    layout="wide",
    page_icon="🛡",
)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
    <div style="padding: 20px; border-radius: 12px;
                background: linear-gradient(90deg, #141E30, #243B55);
                color: white; text-align:center;">
        <h1 style="margin-bottom:5px;">🛡 Real-Time Fraud Detection Dashboard</h1>
        <p style="margin-top:-8px;">AI Powered • Kafka Streaming • Live Detection</p>
    </div>
""", unsafe_allow_html=True)

st.write("")  # spacing

# Load fraud model
model = joblib.load("fraud_model.pkl")

# Kafka Consumer
consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

# Storage for recent transactions
recent_data = []

# ---------------------------
# REAL-TIME PLACEHOLDER AREA
# ---------------------------
stats_placeholder = st.empty()
table_placeholder = st.empty()
chart_placeholder = st.empty()

fraud_count = 0
normal_count = 0
total_count = 0

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("⚙️ Controls")

refresh_rate = st.sidebar.slider("UI Refresh (seconds)", 0.2, 3.0, 0.8)
show_gauge = st.sidebar.checkbox("Show Fraud Gauge", True)
show_chart = st.sidebar.checkbox("Show Timeline Chart", True)

st.sidebar.markdown("---")
st.sidebar.info("📡 Listening to Kafka topic: **transactions**")

# ---------------------------
# MAIN LOOP
# ---------------------------
while True:
    msg_pack = consumer.poll(timeout_ms=500)

    if msg_pack:
        for tp, messages in msg_pack.items():
            for msg in messages:

                tx = msg.value
                total_count += 1

                df = pd.DataFrame([tx])
                df_features = engineer_features(df)

                prediction = model.predict(df_features)[0]
                proba = model.predict_proba(df_features)[0][1]

                if prediction == 1:
                    fraud_count += 1
                else:
                    normal_count += 1

                # Add to recent memory (max 10)
                recent_data.append({
                    "transaction_id": tx["transaction_id"],
                    "country": tx["country"],
                    "amount": tx["amount"],
                    "user_id": tx["user_id"],
                    "timestamp": pd.to_datetime(tx["timestamp"], unit='s'),
                    "fraud_prob": round(proba, 2),
                    "fraud": prediction
                })

                if len(recent_data) > 10:
                    recent_data.pop(0)

                # ---------------------------
                # UPDATE UI
                # ---------------------------

                # METRICS ROW
                with stats_placeholder.container():
                    c1, c2, c3 = st.columns(3)

                    c1.metric("📊 Total Transactions", total_count)
                    c2.metric("⚠️ Fraud Cases", fraud_count)
                    c3.metric("✔ Normal Cases", normal_count)

                # TABLE DISPLAY
                recent_df = pd.DataFrame(recent_data[::-1])
                with table_placeholder.container():
                    st.markdown("### 🔥 Latest Transactions")
                    st.dataframe(
                        recent_df,
                        use_container_width=True,
                        hide_index=True
                    )

                # FRAUD GAUGE
                if show_gauge:
                    gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=proba * 100,
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "red" if prediction == 1 else "green"},
                            "steps": [
                                {"range": [0, 30], "color": "#d4ffd4"},
                                {"range": [30, 70], "color": "#ffffcc"},
                                {"range": [70, 100], "color": "#ffcccc"},
                            ],
                        }
                    ))

                    gauge.update_layout(height=250)

                    st.markdown("### 🎯 Fraud Probability Gauge")
                    st.plotly_chart(gauge, use_container_width=True)

                # LINE CHART
                if show_chart:
                    timeline = pd.DataFrame(recent_data)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=timeline["timestamp"],
                        y=timeline["fraud_prob"],
                        mode="lines+markers",
                        line=dict(color="orange", width=3),
                        marker=dict(size=8)
                    ))
                    fig.update_layout(
                        title="📈 Fraud Probability Over Time",
                        xaxis_title="Time",
                        yaxis_title="Fraud Probability",
                        yaxis_range=[0, 1],
                        height=300,
                    )
                    chart_placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(refresh_rate)
