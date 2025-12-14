import csv, random, time

# Number of rows you want (you can increase to 10,000 also)
TOTAL_ROWS = 50000

with open("historical_transactions.csv", "w", newline="") as f:
    writer = csv.writer(f)

    # header
    writer.writerow(["transaction_id", "amount", "country", "user_id", "timestamp"])

    # generate data
    for _ in range(TOTAL_ROWS):
        writer.writerow([
            random.randint(1000, 9999),
            round(random.uniform(10, 2000), 2),
            random.choice(["IN", "US", "UK", "JP"]),
            random.randint(1, 50),
            time.time()
        ])

print("✔ historical_transactions.csv created successfully!")
