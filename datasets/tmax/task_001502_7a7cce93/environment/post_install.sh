apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/uptime_monitor
    cd /home/user/uptime_monitor
    git init
    git config user.name "SRE Bot"
    git config user.email "sre@example.com"

    # Create initial good state
    cat << 'EOF' > monitor.py
import re

def parse_uptime_log(log_line):
    # Extracts uptime percentage and load average
    match = re.search(r'uptime:\s*(\d+\.?\d*)%\s*-\s*load:\s*(\d+\.?\d*)', log_line)
    if not match:
        raise ValueError(f"Invalid log format: {log_line}")
    return float(match.group(1)), float(match.group(2))
EOF

    cat << 'EOF' > test_monitor.py
import unittest
from monitor import parse_uptime_log

class TestMonitor(unittest.TestCase):
    def test_standard_log(self):
        u, l = parse_uptime_log("INFO: Server UP - uptime: 99.9% - load: 1.5")
        self.assertEqual(u, 99.9)
        self.assertEqual(l, 1.5)

    def test_integer_log(self):
        u, l = parse_uptime_log("INFO: Server UP - uptime: 100% - load: 2")
        self.assertEqual(u, 100.0)
        self.assertEqual(l, 2.0)

    def test_edge_case_whitespace(self):
        # This is the test that will fail after the bad commit
        u, l = parse_uptime_log("INFO: Server UP - uptime: 99.99 % - load: 0.5")
        self.assertEqual(u, 99.99)
        self.assertEqual(l, 0.5)

if __name__ == '__main__':
    unittest.main()
EOF

    git add monitor.py test_monitor.py
    git commit -m "Initial commit: working parser"
    git tag v1.0

    # Add a few dummy commits
    echo "# dummy 1" >> monitor.py
    git commit -am "Add comment 1"

    echo "# dummy 2" >> monitor.py
    git commit -am "Add comment 2"

    # Introduce the bug
    cat << 'EOF' > monitor.py
import re

def parse_uptime_log(log_line):
    # Extracts uptime percentage and load average
    match = re.search(r'uptime:\s*(\d+\.?\d*)% - load:\s*(\d+\.?\d*)', log_line)
    if not match:
        raise ValueError(f"Invalid log format: {log_line}")
    return float(match.group(1)), float(match.group(2))

# dummy 1
# dummy 2
EOF

    git commit -am "Refactor regex to be stricter on delimiters"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Add more dummy commits
    echo "# dummy 3" >> monitor.py
    git commit -am "Add comment 3"

    echo "# dummy 4" >> monitor.py
    git commit -am "Add comment 4"

    # Store the bad commit in a hidden file to verify later easily
    echo $BAD_COMMIT > /tmp/.expected_bad_commit

    chmod -R 777 /home/user
    chmod 777 /tmp/.expected_bad_commit