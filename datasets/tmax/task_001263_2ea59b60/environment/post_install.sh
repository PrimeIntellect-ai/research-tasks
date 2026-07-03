apt-get update && apt-get install -y python3 python3-pip tesseract-ocr tesseract-ocr-eng fonts-liberation
    pip3 install pytest Pillow pytesseract

    # Create directories
    mkdir -p /app
    mkdir -p /home/user/raw_data

    # Generate the image
    cat << 'EOF' > /tmp/gen_image.py
from PIL import Image, ImageDraw, ImageFont
import os

img = Image.new('RGB', (1000, 400), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = """LEGACY LOG SPECIFICATION
========================
Extraction Regex Pattern:
Event=(E-\\d{4}) \\| User=\\[([^\\]]+)\\] \\| Time=([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{3})
Timestamp Format: YYYY/DD/MM HH:MM:SS.mmm
Retry Deduplication Window: 4500 ms"""

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 24)
except:
    font = ImageFont.load_default()

d.text((20,20), text, fill=(0,0,0), font=font)
img.save('/app/schema_spec.png')
EOF
    python3 /tmp/gen_image.py

    # Generate the data
    cat << 'EOF' > /tmp/gen_data.py
import os
import random
from datetime import datetime, timedelta

os.makedirs('/home/user/raw_data', exist_ok=True)

base_time = datetime(2023, 10, 15, 10, 0, 0)
logs = []
golden_records = []

random.seed(42)

for i in range(500):
    user = f"User_@{random.randint(10,99)}-{random.choice(['A','B','C'])}"
    norm_user = ''.join(c.lower() for c in user if c.isalnum())
    event_id = f"E-{random.randint(1000,9999)}"

    # Base event
    offset = random.uniform(0, 3600)
    event_time = base_time + timedelta(seconds=offset)

    # Format: YYYY/DD/MM HH:MM:SS.mmm
    time_str = event_time.strftime("%Y/%d/%m %H:%M:%S.%f")[:-3]
    log_line = f"INFO: System process. Event={event_id} | User=[{user}] | Time={time_str} | Status=OK\n"
    logs.append((event_time, log_line))

    # Golden record expectation
    iso_time = event_time.isoformat()
    golden_records.append((event_time, f"[{iso_time}] EVENT:{event_id} USER:{norm_user}"))

    # Simulate duplicates (within 4500ms)
    if random.random() < 0.4:
        dup_time = event_time + timedelta(milliseconds=random.randint(500, 4000))
        dup_time_str = dup_time.strftime("%Y/%d/%m %H:%M:%S.%f")[:-3]
        # slightly malformed token but normalizes to same
        dup_user = user + "$"
        dup_log_line = f"INFO: System process. Event={event_id} | User=[{dup_user}] | Time={dup_time_str} | Status=RETRY\n"
        logs.append((dup_time, dup_log_line))

# Shuffle and write to multiple files
random.shuffle(logs)
chunk_size = len(logs) // 3
for idx, chunk in enumerate([logs[i:i + chunk_size] for i in range(0, len(logs), chunk_size)]):
    with open(f'/home/user/raw_data/log_{idx}.txt', 'w') as f:
        for _, line in chunk:
            f.write(line)

# Sort golden records chronologically
golden_records.sort(key=lambda x: x[0])
with open('/tmp/golden_events.txt', 'w') as f:
    for _, line in golden_records:
        f.write(line + "\n")
EOF
    python3 /tmp/gen_data.py

    # Create verify script
    cat << 'EOF' > /tmp/verify.py
import sys

def load_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

agent_data = load_data('/home/user/clean_events.txt')
golden_data = load_data('/tmp/golden_events.txt')

if not agent_data:
    print("F1=0.0")
    sys.exit(0)

true_positives = len(agent_data.intersection(golden_data))
false_positives = len(agent_data - golden_data)
false_negatives = len(golden_data - agent_data)

precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

if precision + recall == 0:
    f1 = 0.0
else:
    f1 = 2 * (precision * recall) / (precision + recall)

print(f"F1={f1:.4f}")
EOF

    # Cleanup temporary scripts
    rm /tmp/gen_image.py /tmp/gen_data.py

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user