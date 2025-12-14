import pandas as pd

def engineer_features(df):
    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    # Time-based features
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek

    # Encode country
    df["country_code"] = df["country"].astype("category").cat.codes

    # High amount flag (threshold = 1000)
    df["is_high_amount"] = (df["amount"] > 1000).astype(int)

    # User average transaction amount (historical)
    user_avg = df.groupby("user_id")["amount"].transform("mean")

    df["user_avg_amount"] = user_avg
    df["amount_diff_from_avg"] = df["amount"] - user_avg

    # Select only final feature columns
    return df[[
        "amount",
        "country_code",
        "hour",
        "day_of_week",
        "is_high_amount",
        "user_avg_amount",
        "amount_diff_from_avg"
    ]]
