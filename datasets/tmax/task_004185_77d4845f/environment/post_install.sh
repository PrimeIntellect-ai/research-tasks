apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    mkdir -p /home/user/diagnostics_tool
    cd /home/user/diagnostics_tool
    git init
    git config user.email "admin@example.com"
    git config user.name "Admin"

    cat << 'EOF' > sync.py
import os
from datetime import datetime, timedelta

def process_data():
    secret = os.environ.get("API_SECRET")
    if secret != "sec_r3v3al3d_9921":
        print("ERROR: Unauthorized")
        return

    timestamp = "2023-10-27 15:00:00"
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    # Target UTC hour is 10
    expected_utc_hour = 10

    # Adjust time iteratively
    iterations = 0
    while dt.hour != expected_utc_hour:
        dt -= timedelta(hours=2) # BUG: skips over 10 (15 -> 13 -> 11 -> 9)
        iterations += 1
        if iterations > 50:
             print("Error: Convergence failure adjusting timezone.")
             return

    with open("/home/user/diagnostic_report.txt", "w") as f:
        f.write(f"Synced UTC Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    process_data()
EOF

    git add sync.py
    git commit -m "Initial commit with sync logic"

    cat << 'EOF' > credentials.json
{"API_SECRET": "sec_r3v3al3d_9921"}
EOF
    git add credentials.json
    git commit -m "Add credentials"

    git rm credentials.json
    git commit -m "Remove credentials"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user