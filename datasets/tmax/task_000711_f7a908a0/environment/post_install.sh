apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest pandas

useradd -m -s /bin/bash user || true

cat << 'EOF' > /tmp/setup.py
import json
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

metadata = [
    {"string_id": "btn_submit", "module": "checkout", "priority": "high"},
    {"string_id": "lbl_title", "module": "home", "priority": "low"},
    {"string_id": "msg_error", "module": "core", "priority": "high"},
    {"string_id": "btn_cancel", "module": "checkout", "priority": "medium"},
    {"string_id": "txt_desc", "module": "catalog", "priority": "low"},
    {"string_id": "err_network", "module": "core", "priority": "high"}
]

with open("/home/user/string_metadata.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["string_id", "module", "priority"])
    writer.writeheader()
    writer.writerows(metadata)

langs = ["fr-FR", "es-ES", "de-DE", "ja-JP"]
start_time = datetime(2023, 10, 25, 0, 0, 0)

with open("/home/user/telemetry.jsonl", "w") as f:
    for i in range(10000):
        dt = start_time + timedelta(seconds=random.randint(0, 86399))
        record = {
            "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "lang": random.choice(langs),
            "string_id": random.choice(metadata)["string_id"]
        }
        f.write(json.dumps(record) + "\n")
EOF

python3 /tmp/setup.py
rm /tmp/setup.py

chmod -R 777 /home/user