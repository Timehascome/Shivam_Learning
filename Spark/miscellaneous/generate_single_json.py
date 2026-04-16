import json
import os
import random
from datetime import datetime, timedelta

OUT_DIR = "raw_json_data"
os.makedirs(OUT_DIR, exist_ok=True)

users = ["u1", "u2", "u3", "u4", "u5"]
actions = ["view", "add_to_cart", "purchase"]
countries = ["IN", "SG", "US"]
devices = ["android", "ios", "web"]

start = datetime(2026, 1, 18, 10, 10, 0)

def make_event(i: int):
    ts = start + timedelta(seconds=i * random.randint(5, 25))
    action = random.choice(actions)
    amount = 0 if action != "purchase" else random.choice([199, 499, 1299, 2499])
    return {
        "event_time": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": random.choice(users),
        "action": action,
        "amount": amount,
        "country": random.choice(countries),
        "device": random.choice(devices),
        "metadata": {
            "ip": ".".join(str(random.randint(1, 255)) for _ in range(4)),
            "campaign": random.choice(["newyear", "brand", "sale", "push", "organic"])
        }
    }

# 1) single file
with open(os.path.join(OUT_DIR, "events_single.json"), "w", encoding="utf-8") as f:
    for i in range(200):
        f.write(json.dumps(make_event(i)) + "\n")

# # 2) multiple files
# for part in range(5):
#     path = os.path.join(OUT_DIR, f"events_part_{part}.json")
#     with open(path, "w", encoding="utf-8") as f:
#         for i in range(100):
#             f.write(json.dumps(make_event(part * 100 + i)) + "\n")

print(f"Created JSONL files under: {OUT_DIR}/")