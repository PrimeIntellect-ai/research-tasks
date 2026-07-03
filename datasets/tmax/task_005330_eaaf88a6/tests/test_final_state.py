# test_final_state.py

import os
import re
import subprocess
import time
import pytest

def test_fstab_configured():
    path = "/home/user/ota_payload/etc/fstab"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check for the required mount entry
    pattern = re.compile(r"^/dev/mmcblk0p3\s+/var/spool/iot_data\s+ext4\s+.*usrquota.*", re.MULTILINE)
    assert pattern.search(content), "fstab does not contain the required mount entry for /dev/mmcblk0p3 to /var/spool/iot_data with ext4 and usrquota options."

def test_iptables_rules():
    path = "/home/user/ota_payload/etc/iptables.rules"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check for the required iptables rule components
    assert "-t nat" in content, "iptables rule must specify the 'nat' table."
    assert "PREROUTING" in content, "iptables rule must append or insert to the 'PREROUTING' chain."
    assert "-p tcp" in content, "iptables rule must specify the TCP protocol."
    assert "--dport 80" in content, "iptables rule must specify destination port 80."
    assert "-j REDIRECT" in content, "iptables rule must use the REDIRECT target."
    assert "--to-port 8080" in content, "iptables rule must redirect to port 8080."

def test_metric_execution_time():
    executable = "/home/user/edge-aggregator"
    assert os.path.isfile(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

    test_csv = "/tmp/hidden_eval.csv"
    if not os.path.exists(test_csv):
        # Generate a ~500MB CSV file for testing
        chunk = b"1672531200,sensor_1,25.4\n" * 100000  # ~2.5MB per chunk
        with open(test_csv, "wb") as f:
            for _ in range(200):
                f.write(chunk)

    start_time = time.perf_counter()
    result = subprocess.run([executable, test_csv, "/dev/null"], capture_output=True)
    end_time = time.perf_counter()

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}:\n{result.stderr.decode()}"

    runtime = end_time - start_time
    assert runtime <= 1.5, f"Execution runtime {runtime:.4f}s exceeds the threshold of 1.5s. Ensure the code is compiled with -O3."