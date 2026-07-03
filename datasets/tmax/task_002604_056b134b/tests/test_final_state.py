# test_final_state.py
import os
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_inventory.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_execution():
    script_path = "/home/user/process_inventory.sh"
    # Run the script to generate the files, in case the student hasn't run it
    if os.path.isfile(script_path) and os.access(script_path, os.X_OK):
        # Remove output files if they exist to ensure a fresh run
        for f in ["/home/user/process.log", "/home/user/active_servers.conf"]:
            if os.path.exists(f):
                os.remove(f)
        result = subprocess.run([script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed to execute properly. Error: {result.stderr}"

def test_process_log_contents():
    log_path = "/home/user/process.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    expected_log = """[INFO] Pipeline started
[INFO] Dropped rows with embedded newlines: 3
[INFO] Total unique servers after deduplication: 4
[INFO] Active servers written to config: 3
[INFO] Pipeline finished"""

    with open(log_path, "r") as f:
        actual_log = f.read().strip()

    assert actual_log == expected_log, f"Log file contents do not match expected metrics.\nExpected:\n{expected_log}\nActual:\n{actual_log}"

def test_active_servers_conf_contents():
    conf_path = "/home/user/active_servers.conf"
    assert os.path.isfile(conf_path), f"Config file {conf_path} was not created."

    expected_conf = """[web-front-01]
ServerID=101
OperatingSystem=UBUNTU
Info=Primary web node, upgraded
---
[lb-01]
ServerID=106
OperatingSystem=HAPROXY
Info=Load balancer
---
[worker-node]
ServerID=105
OperatingSystem=ALPINE
Info=Background jobs (migrated)
---"""

    with open(conf_path, "r") as f:
        actual_conf = f.read().strip()

    assert actual_conf == expected_conf, f"Config file contents do not match expected output.\nExpected:\n{expected_conf}\nActual:\n{actual_conf}"