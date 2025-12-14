import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from feature_engineering import engineer_features

# Load historical data
df = pd.read_csv("historical_transactions.csv")

# Apply feature engineering
features = engineer_features(df)

# IMPROVED FRAUD LOGIC
df["label"] = (
    (df["amount"] > 1500) |
    ((df["country"] == "JP") & (df["amount"] > 1200)) |
    ((df["user_id"] > 40) & (df["amount"] > 900)) |
    ((df["hour"] > 22) & (df["amount"] > 700))
).astype(int)

y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    features, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=200)
model.fit(X_train, y_train)

print("Training accuracy:", model.score(X_train, y_train))
print("Testing accuracy:", model.score(X_test, y_test))

# Save the model
joblib.dump(model, "fraud_model.pkl")
print("✔ Model saved as fraud_model.pkl")
