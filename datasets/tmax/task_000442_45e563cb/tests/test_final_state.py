# test_final_state.py

import os
import re
import pytest

def test_operator_py_exists():
    assert os.path.exists("/home/user/operator.py"), "/home/user/operator.py does not exist."
    assert os.path.isfile("/home/user/operator.py"), "/home/user/operator.py is not a file."

def test_supervisor_sh_exists():
    assert os.path.exists("/home/user/supervisor.sh"), "/home/user/supervisor.sh does not exist."
    assert os.path.isfile("/home/user/supervisor.sh"), "/home/user/supervisor.sh is not a file."

def test_operator_log_format():
    log_file = "/home/user/operator.log"
    assert os.path.exists(log_file), f"{log_file} does not exist. Did you run supervisor.sh?"

    with open(log_file, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"Expected exactly 3 lines in {log_file}, found {len(lines)}."

    pattern = re.compile(r"^GW: (?P<ip>[0-9\.]+) \| PING: (?P<ping>SUCCESS|FAILURE) \| STORAGE: (?P<storage>\d+) KB \| STATUS: (?P<status>HEALTHY|UNHEALTHY)$")

    for i, line in enumerate(lines):
        match = pattern.match(line)
        assert match, f"Line {i+1} in {log_file} does not match the expected format: '{line}'"

        # Verify status logic
        ping = match.group("ping")
        storage = int(match.group("storage"))
        status = match.group("status")

        expected_status = "HEALTHY" if ping == "SUCCESS" and storage <= 10240 else "UNHEALTHY"
        assert status == expected_status, f"Line {i+1} has incorrect STATUS '{status}'. Expected '{expected_status}' based on PING '{ping}' and STORAGE '{storage}'."

def test_supervisor_sh_contents():
    with open("/home/user/supervisor.sh", "r") as f:
        content = f.read()

    assert "sleep 1" in content or "sleep 1s" in content, "supervisor.sh does not seem to contain a 1-second sleep."
    assert "operator.py" in content, "supervisor.sh does not seem to execute operator.py."