apt-get update && apt-get install -y python3 python3-pip redis-server curl
    pip3 install --default-timeout=100 pytest flask gunicorn jupyter scipy numpy redis

    mkdir -p /app/api
    mkdir -p /app/notebooks
    mkdir -p /app/data
    mkdir -p /app/oracle

    # Create empirical data
    echo "t,N" > /app/data/empirical.csv
    echo "0,10" >> /app/data/empirical.csv
    echo "1,11" >> /app/data/empirical.csv

    # Create oracle binary
    cat << 'EOF' > /app/oracle/integrator_reference
#!/usr/bin/env python3
import sys, json
with open(sys.argv[1]) as f:
    d = json.load(f)
out = {"result": d["N_initial"] * d["growth_rate"]}
with open(sys.argv[2], 'w') as f:
    json.dump(out, f)
EOF
    chmod +x /app/oracle/integrator_reference

    # Create API app
    cat << 'EOF' > /app/api/app.py
from flask import Flask
app = Flask(__name__)
@app.route('/simulate', methods=['POST'])
def simulate():
    return "OK", 200
EOF

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app