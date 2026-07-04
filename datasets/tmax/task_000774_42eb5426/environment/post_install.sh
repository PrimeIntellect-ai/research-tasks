apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user
    cat << 'EOF' > /home/user/process_time.py
import sys
from datetime import datetime

if len(sys.argv) != 2:
    sys.exit(0)

ts_str = sys.argv[1]
try:
    dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M")
    # Simulate a DST ambiguous time crash for America/Chicago (Fall back)
    if dt.year == 2023 and dt.month == 11 and dt.day == 5 and dt.hour == 1 and dt.minute == 15:
        sys.stderr.write("AmbiguousTimeError: 2023-11-05 01:15 is ambiguous in America/Chicago\n")
        sys.exit(1)
    sys.exit(0)
except Exception:
    sys.exit(0)
EOF
    chmod +x /home/user/process_time.py

    # Generate timestamps
    python3 -c '
import random
from datetime import datetime, timedelta

start = datetime(2023, 1, 1)
timestamps = set()
while len(timestamps) < 499:
    random_days = random.randint(0, 360)
    random_minutes = random.randint(0, 24*60 - 1)
    dt = start + timedelta(days=random_days, minutes=random_minutes)
    if not (dt.month == 11 and dt.day == 5 and dt.hour == 1):
        timestamps.add(dt.strftime("%Y-%m-%d %H:%M"))

timestamps_list = list(timestamps)
timestamps_list.insert(random.randint(0, 499), "2023-11-05 01:15")

with open("/home/user/timestamps.txt", "w") as f:
    for ts in timestamps_list:
        f.write(ts + "\n")
'

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user