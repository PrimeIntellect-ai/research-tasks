apt-get update && apt-get install -y python3 python3-pip git python-is-python3
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/telemetry_repo
cd /home/user/telemetry_repo
git init
git config user.name "Auto Test"
git config user.email "test@example.com"

# Create the initial working process_telemetry.py
cat << 'EOF' > process_telemetry.py
import json
from datetime import datetime, timezone
import sys

def process_event(event_data):
    ts = float(event_data['timestamp'])
    # Parse as timezone-aware UTC datetime
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)

    now = datetime.now(timezone.utc)
    delay = (now - dt).total_seconds()

    return json.dumps({
        "time": dt.isoformat(),
        "value": event_data['value'],
        "delay": delay
    })

if __name__ == '__main__':
    try:
        data = json.loads(sys.argv[1])
        print(process_event(data))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
EOF

git add process_telemetry.py
git commit -m "Initial commit: add telemetry processor"

# Add 120 good commits
for i in $(seq 1 120); do
    echo "Update $i" > dummy.txt
    git add dummy.txt
    git commit -m "Dummy update $i"
done

# Introduce the bug at commit 121
cat << 'EOF' > process_telemetry.py
import json
from datetime import datetime, timezone
import sys

def process_event(event_data):
    ts = float(event_data['timestamp'])
    # Bug: utcfromtimestamp returns a naive datetime (drops timezone awareness)
    dt = datetime.utcfromtimestamp(ts)

    now = datetime.now(timezone.utc)
    # This will crash: TypeError: can't subtract offset-naive and offset-aware datetimes
    delay = (now - dt).total_seconds()

    return json.dumps({
        "time": dt.isoformat(),
        "value": event_data['value'],
        "delay": delay
    })

if __name__ == '__main__':
    try:
        data = json.loads(sys.argv[1])
        print(process_event(data))
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

git add process_telemetry.py
git commit -m "Refactor datetime parsing for timezone issues"
BAD_COMMIT=$(git rev-parse HEAD)

# Add 50 more commits
for i in $(seq 122 170); do
    echo "Update $i" > dummy.txt
    git add dummy.txt
    git commit -m "Dummy update $i"
done

# Save the bad commit hash somewhere the verification script can find it
echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

chmod -R 777 /home/user
chmod 777 /tmp/expected_bad_commit.txt