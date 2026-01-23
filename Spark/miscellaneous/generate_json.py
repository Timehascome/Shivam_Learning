import json
import os
import random
from datetime import datetime, timedelta

# Output directory
OUTPUT_DIR = "C://Users//399sh//Downloads//Learning//Spark//data_in"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sample values
actions = ["click", "view", "purchase", "refund"]

def generate_event():
    event_time = (
        datetime.now() - timedelta(minutes=random.randint(1, 500))
    ).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "event_time": event_time,      # StringType
        "user_id": f"user_{random.randint(1, 100)}",  # StringType
        "action": random.choice(actions),              # StringType
        "amount": random.randint(10, 5000)             # IntegerType
    }

# Generate 10 JSON files
for i in range(1, 11):
    file_path = os.path.join(OUTPUT_DIR, f"event_{i}.json")
    with open(file_path, "w") as f:
        json.dump(generate_event(), f, indent=4)

print("✅ 10 JSON files generated in 'sample_events/' folder")
