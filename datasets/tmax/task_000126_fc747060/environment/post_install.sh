apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest pillow pyjwt pandas scikit-learn

mkdir -p /app /truth /home/user

cat << 'EOF' > /tmp/generate.py
import os
import jwt
import random
import base64
import json
import csv
from PIL import Image, ImageDraw

# Create image
img = Image.new('RGB', (600, 100), color=(73, 109, 137))
d = ImageDraw.Draw(img)
d.text((10, 10), "LEGACY GATEWAY SECRET: 'ComplianceAuditKey2023!'", fill=(255, 255, 0))
img.save('/app/architecture.png')

users = [f"user{i}" for i in range(100)]
secret_weak = "ComplianceAuditKey2023!"
secret_strong = "SuperSecretSecureKey2024!"

tokens = []
ssh_logs = []
ground_truth = []

# Generate SSH logs
for u in users:
    fingerprint = f"SHA256:{base64.b64encode(str(random.random()).encode()).decode()[:43]}"
    ssh_logs.append(f"Accepted publickey for {u} from 10.0.0.1 port 22 ssh2: RSA {fingerprint}")

with open('/app/ssh_logs.txt', 'w') as f:
    f.write('\n'.join(ssh_logs))

def create_alg_none(payload):
    header = {"alg": "none", "typ": "JWT"}
    encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    return f"{encoded_header}.{encoded_payload}."

for i in range(5000):
    user = random.choice(users)
    token_id = f"tok_{i}"
    vuln_type = random.choice(["alg_none", "weak_signature", "expired", "valid"])

    payload = {"sub": user, "jti": token_id, "exp": 1800000000}

    if vuln_type == "alg_none":
        token = create_alg_none(payload)
        ground_truth.append((token_id, vuln_type))
    elif vuln_type == "weak_signature":
        token = jwt.encode(payload, secret_weak, algorithm="HS256")
        ground_truth.append((token_id, vuln_type))
    elif vuln_type == "expired":
        payload["exp"] = 1700000000
        token = jwt.encode(payload, secret_strong, algorithm="HS256")
        ground_truth.append((token_id, vuln_type))
    else:
        token = jwt.encode(payload, secret_strong, algorithm="HS256")

    tokens.append(token)

with open('/app/tokens.txt', 'w') as f:
    f.write('\n'.join(tokens))

with open('/truth/ground_truth.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["token_id", "vulnerability_type"])
    writer.writerows(ground_truth)
EOF

python3 /tmp/generate.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app /truth