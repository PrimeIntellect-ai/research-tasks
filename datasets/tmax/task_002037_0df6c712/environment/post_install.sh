apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest pandas cryptography

    # Temporarily install PyJWT to generate the dataset
    pip3 install PyJWT

    cat << 'EOF' > /tmp/gen.py
import json, random, jwt, string, os, pandas as pd

os.makedirs('/home/user/logs', exist_ok=True)
os.makedirs('/home/user/wordlists', exist_ok=True)
os.makedirs('/truth', exist_ok=True)

words = ["password123", "admin", "secret", "qwerty", "123456", "letmein", "dragon", "baseball", "monkey", "shadow"]
words += [''.join(random.choices(string.ascii_lowercase, k=6)) for _ in range(90)]
with open('/home/user/wordlists/weak_secrets.txt', 'w') as f:
    f.write('\n'.join(words))

logs = []
truth = []

for i in range(10000):
    kid = f"key_{i}"
    if random.random() < 0.05:
        secret = random.choice(words)
        token = jwt.encode({"user": f"user_{i}"}, secret, algorithm="HS256", headers={"kid": kid})
        truth.append({"id": kid, "secret": secret})
    else:
        secret = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        token = jwt.encode({"user": f"user_{i}"}, secret, algorithm="HS256", headers={"kid": kid})
    logs.append({"id": kid, "token": token})

with open('/home/user/logs/jwt_audit.json', 'w') as f:
    json.dump(logs, f)

pd.DataFrame(truth).to_csv('/truth/ground_truth_jwts.csv', index=False)
EOF

    python3 /tmp/gen.py
    pip3 uninstall -y PyJWT

    # Setup the vendored PyJWT package
    mkdir -p /app
    git clone --branch 2.8.0 https://github.com/jpadilla/pyjwt.git /app/PyJWT

    # Introduce the perturbation
    if [ -f /app/PyJWT/pyproject.toml ]; then
        sed -i -E 's/cryptography>=[0-9\.]+/cryptography>=999.0.0/g' /app/PyJWT/pyproject.toml
        if ! grep -q "cryptography>=999.0.0" /app/PyJWT/pyproject.toml; then
            # If there wasn't a cryptography constraint, add one to the requires list
            sed -i 's/requires = \[/requires = \["cryptography>=999.0.0", /g' /app/PyJWT/pyproject.toml
        fi
    else
        echo '[build-system]' > /app/PyJWT/pyproject.toml
        echo 'requires = ["setuptools", "cryptography>=999.0.0"]' >> /app/PyJWT/pyproject.toml
        echo 'build-backend = "setuptools.build_meta"' >> /app/PyJWT/pyproject.toml
    fi

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app /truth