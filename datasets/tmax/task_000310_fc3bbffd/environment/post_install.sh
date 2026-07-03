apt-get update && apt-get install -y python3 python3-pip tesseract-ocr gcc
    pip3 install pytest Pillow pandas

    mkdir -p /app
    mkdir -p /home/user/data

    cat << 'EOF' > /tmp/setup.py
import os
import csv
import random
from PIL import Image, ImageDraw

os.makedirs('/app', exist_ok=True)
os.makedirs('/home/user/data', exist_ok=True)

# Generate Base Config Image
img = Image.new('RGB', (400, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = "SERVER, PARAM, VALUE\nALPHA, fan_speed, 3000.0\nALPHA, temp_limit, 80.0\nBETA, fan_speed, 3200.0\nBETA, temp_limit, 85.0"
d.text((10,10), text, fill=(0,0,0))
img.save('/app/base_config.png')

# Generate Deltas
base_time = 1672531200
random.seed(42)

state = {
    'ALPHA': {'fan_speed': 3000.0, 'temp_limit': 80.0},
    'BETA': {'fan_speed': 3200.0, 'temp_limit': 85.0}
}

deltas = []
for _ in range(100):
    ts = base_time + random.randint(100, 86000)
    srv = random.choice(['ALPHA', 'BETA'])
    prm = random.choice(['fan_speed', 'temp_limit'])
    val = state[srv][prm] + random.uniform(-10.0, 10.0)
    val = round(val, 1)
    state[srv][prm] = val
    deltas.append((ts, srv, prm, val))

deltas.sort(key=lambda x: x[0])

with open('/home/user/data/deltas.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp','server_id','param_name','new_value'])
    for d in deltas:
        writer.writerow(d)

# Generate Reference Output
ref_state = {
    'ALPHA': {'fan_speed': 3000.0, 'temp_limit': 80.0},
    'BETA': {'fan_speed': 3200.0, 'temp_limit': 85.0}
}

output = []
delta_idx = 0
for h in range(24):
    end_ts = base_time + (h + 1) * 3600 - 1
    while delta_idx < len(deltas) and deltas[delta_idx][0] <= end_ts:
        _, srv, prm, val = deltas[delta_idx]
        ref_state[srv][prm] = val
        delta_idx += 1
    output.append([
        h, 
        ref_state['ALPHA']['fan_speed'], 
        ref_state['ALPHA']['temp_limit'],
        ref_state['BETA']['fan_speed'], 
        ref_state['BETA']['temp_limit']
    ])

with open('/home/user/reference.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['hour_index','ALPHA_fan_speed','ALPHA_temp_limit','BETA_fan_speed','BETA_temp_limit'])
    for row in output:
        writer.writerow(row)
EOF

    python3 /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app