apt-get update && apt-get install -y python3 python3-pip python3-setuptools
    pip3 install pytest

    # Create directories
    mkdir -p /app/vendored/pysm-lib/pysm
    mkdir -p /app/oracle

    # Create vendored package setup.py
    cat << 'EOF' > /app/vendored/pysm-lib/setup.py
from setuptools import setup, find_packages

setup(
    name='pysm-lib',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'typing-extensions==4.0.0',
        'typing-extensions>=4.5.0'
    ]
)
EOF

    # Create vendored package init
    touch /app/vendored/pysm-lib/pysm/__init__.py

    # Create oracle legacy parser
    cat << 'EOF' > /app/oracle/legacy_parser
#!/usr/bin/env python3
import sys

def main():
    state = "IDLE"
    acc = 0
    for line in sys.stdin:
        parts = line.strip().split()
        if not parts:
            continue
        cmd = parts[0]

        if cmd == "INIT":
            if len(parts) == 2:
                try:
                    val = int(parts[1])
                    state = "ACTIVE"
                    acc = val
                except ValueError:
                    print("ERROR: UNKNOWN_CMD")
            else:
                print("ERROR: UNKNOWN_CMD")
        elif cmd in ("ADD", "MUL"):
            if state == "IDLE":
                print("ERROR: INVALID_STATE")
            else:
                if len(parts) == 2:
                    try:
                        val = int(parts[1])
                        if cmd == "ADD":
                            acc += val
                        else:
                            acc *= val
                    except ValueError:
                        print("ERROR: UNKNOWN_CMD")
                else:
                    print("ERROR: UNKNOWN_CMD")
        elif cmd == "EMIT":
            if state == "IDLE":
                print("ERROR: INVALID_STATE")
            else:
                print(f"RESULT: {acc}")
                state = "IDLE"
        else:
            print("ERROR: UNKNOWN_CMD")

if __name__ == "__main__":
    main()
EOF
    chmod +x /app/oracle/legacy_parser

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user