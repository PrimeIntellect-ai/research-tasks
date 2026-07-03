apt-get update && apt-get install -y python3 python3-pip redis-server libhiredis-dev libcurl4-openssl-dev curl
pip3 install pytest pandas flask

mkdir -p /app

cat << 'EOF' > /app/generate_data.py
import random

random.seed(42)

hierarchy = {i: random.randint(1, i-1) for i in range(2, 1001)}
resources = {f"R{i}": random.randint(1, 1000) for i in range(1, 5001)}

with open("/app/redis_cmds.txt", "w") as f:
    for emp, mgr in hierarchy.items():
        f.write(f"SET mgr:{emp} {mgr}\n")
    for res, owner in resources.items():
        f.write(f"SET owner:{res} {owner}\n")

def is_authorized(user, res):
    owner = resources[res]
    if user == owner: return True
    curr = owner
    while curr in hierarchy:
        curr = hierarchy[curr]
        if curr == user: return True
    return False

logs = []
ts = 1600000000

# normal logs
for _ in range(190000):
    res = f"R{random.randint(1, 5000)}"
    owner = resources[res]
    user = owner
    logs.append((ts, user, res))
    ts += random.randint(0, 2)

# inject 150 violations
violations = []
for _ in range(150):
    user = random.randint(1, 1000)
    res = f"R{random.randint(1, 5000)}"
    while is_authorized(user, res):
        user = random.randint(1, 1000)
        res = f"R{random.randint(1, 5000)}"

    start_ts = ts
    logs.append((start_ts, user, res))
    logs.append((start_ts + 10, user, res))
    logs.append((start_ts + 20, user, res))
    violations.append((user, start_ts + 20))
    ts += 100

logs.sort(key=lambda x: x[0])

with open("/app/logs.csv", "w") as f:
    for l in logs:
        f.write(f"{l[0]},{l[1]},{l[2]}\n")

with open("/app/ground_truth.csv", "w") as f:
    for v in violations:
        f.write(f"{v[0]},{v[1]}\n")
EOF

python3 /app/generate_data.py

cat << 'EOF' > /app/api.py
from flask import Flask, Response
app = Flask(__name__)

@app.route('/logs')
def logs():
    def generate():
        with open('/app/logs.csv', 'r') as f:
            for line in f:
                yield line
    return Response(generate(), mimetype='text/csv')

if __name__ == '__main__':
    app.run(port=8080)
EOF

cat << 'EOF' > /app/start_services.sh
#!/bin/bash
redis-server --daemonize yes
sleep 1
cat /app/redis_cmds.txt | redis-cli > /dev/null
python3 /app/api.py &
EOF
chmod +x /app/start_services.sh

cat << 'EOF' > /app/evaluate.py
import sys
import pandas as pd

def load_data(path):
    try:
        df = pd.read_csv(path, header=None, names=['user_id', 'timestamp'])
        return set(tuple(x) for x in df.to_numpy())
    except:
        return set()

truth = load_data('/app/ground_truth.csv')
preds = load_data('/home/user/flagged.csv')

if not truth and not preds:
    print("f1=0.0")
    sys.exit(1)

tp = len(truth.intersection(preds))
fp = len(preds - truth)
fn = len(truth - preds)

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print(f"F1 Score: {f1}")
if f1 >= 0.95:
    sys.exit(0)
else:
    sys.exit(1)
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app