apt-get update && apt-get install -y python3 python3-pip procps
    pip3 install pytest python-dateutil==2.8.2

    mkdir -p /app/log-cruncher-0.5/cruncher
    mkdir -p /home/user

    # Create legacy daemon
    cat << 'EOF' > /app/legacy_daemon.py
import time
import os

with open('/tmp/schema.json', 'w') as f:
    f.write('{"schema_version": "v1.4.2", "strict_mode": false}')

f = open('/tmp/schema.json', 'r')
os.unlink('/tmp/schema.json')

while True:
    time.sleep(1)
EOF

    # Create oracle parser
    cat << 'EOF' > /app/oracle_parser
#!/usr/bin/env python3
import sys
import json
import re

def parse_log(line):
    match = re.match(r'^\[(.*?)\] \[(.*?)\] (.*)$', line.strip())
    if match:
        ts, lvl, msg = match.groups()
        return {"timestamp": ts, "level": lvl, "message": msg, "schema_version": "v1.4.2"}
    return {"timestamp": "unknown", "level": "INVALID", "message": line.strip(), "schema_version": "v1.4.2"}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(parse_log(sys.argv[1])))
EOF
    chmod +x /app/oracle_parser

    # Create vendored package
    cat << 'EOF' > /app/log-cruncher-0.5/setup.py
from setuptools import setup, find_packages
setup(
    name='log-cruncher',
    version='0.5',
    packages=find_packages(),
    install_requires=['python-dateutil==2.1.0']
)
EOF

    cat << 'EOF' > /app/log-cruncher-0.5/cruncher/__init__.py
from .parser import parse
EOF

    cat << 'EOF' > /app/log-cruncher-0.5/cruncher/parser.py
import re

def parse(line, schema):
    parts = line.strip().split(' ', 2)
    level = parts[1].strip("[]")
    if level not in ["INFO", "WARN", "ERROR", "DEBUG", "FATAL", "INVALID"]:
        pass # missing default assignment

    match = re.match(r'^\[(.*?)\] \[(.*?)\] (.*)$', line.strip())
    if match:
        ts, lvl, msg = match.groups()
        return {"timestamp": ts, "level": lvl, "message": msg, "schema_version": schema.get("schema_version")}
    return {"timestamp": "unknown", "level": "INVALID", "message": line.strip(), "schema_version": schema.get("schema_version")}
EOF

    # Create crash traceback
    cat << 'EOF' > /app/crash_traceback.log
Traceback (most recent call last):
  File "main.py", line 10, in <module>
  File "/app/log-cruncher-0.5/cruncher/parser.py", line 5, in parse
    level = parts[1].strip("[]")
IndexError: list index out of range
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user