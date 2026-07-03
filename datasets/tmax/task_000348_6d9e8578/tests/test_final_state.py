# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/sanitize.py"
ORACLE_SCRIPT = "/app/oracle_sanitize.py"
LOG_FILE = "/tmp/artifact_db.log"

def generate_random_path(length, absolute=False):
    chars = string.ascii_letters + string.digits + "_-"
    parts = []
    current_len = 0
    while current_len < length:
        part_len = random.randint(1, 10)
        part = ''.join(random.choices(chars, k=part_len))
        parts.append(part)
        current_len += part_len + 1
    path = "/".join(parts)[:length]
    if absolute and not path.startswith("/"):
        path = "/" + path.lstrip("/")
    return path

def generate_manifest_line():
    length = random.randint(5, 50)
    chars = string.ascii_letters + string.digits + "_-."

    if random.random() < 0.5:
        # malicious or edge cases
        malicious_parts = ["../", "..", "/../", "/"]
        part = random.choice(malicious_parts)
        rest_len = max(1, length - len(part))
        rest = ''.join(random.choices(chars + "/", k=rest_len))
        if part == "/":
            return part + rest
        else:
            mid = len(rest) // 2
            return rest[:mid] + part + rest[mid:]
    else:
        return ''.join(random.choices(chars + "/", k=length))

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script not found at {ORACLE_SCRIPT}"

    random.seed(42)

    # clear log file if exists to ensure we only check new logs
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    total_expected_lines = 0

    for i in range(100):
        target_dir = generate_random_path(random.randint(10, 30), absolute=True)
        manifest_lines = [generate_manifest_line() for _ in range(random.randint(10, 50))]

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            for line in manifest_lines:
                f.write(line + "\n")
            manifest_path = f.name

        try:
            oracle_cmd = ["python3", ORACLE_SCRIPT, target_dir, manifest_path]
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)

            agent_cmd = ["python3", AGENT_SCRIPT, target_dir, manifest_path]
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

            oracle_out = oracle_res.stdout.strip()
            agent_out = agent_res.stdout.strip()

            if oracle_out != agent_out:
                pytest.fail(
                    f"Mismatch on iteration {i}.\n"
                    f"Target dir: {target_dir}\n"
                    f"Manifest:\n{chr(10).join(manifest_lines)}\n"
                    f"Oracle output:\n{oracle_out}\n"
                    f"Agent output:\n{agent_out}"
                )

            if oracle_out:
                total_expected_lines += len(oracle_out.split('\n'))

        finally:
            os.remove(manifest_path)

    # Check if log file is created and has content
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} was not created by the agent script"
    with open(LOG_FILE, 'r') as f:
        log_content = f.read().strip()

    if total_expected_lines > 0:
        assert len(log_content) > 0, "Log file is empty but there should be logged paths"
        assert "[SECURE-BIN-84]" in log_content, "Log file does not contain the expected repo ID"
        log_lines = log_content.split('\n')
        assert len(log_lines) == total_expected_lines, f"Log file has {len(log_lines)} lines, expected {total_expected_lines}"

def test_agent_uses_file_locking():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    with open(AGENT_SCRIPT, 'r') as f:
        content = f.read()
    assert "fcntl" in content, "The script does not import or use fcntl"
    assert "flock" in content, "The script does not use flock for file locking as required"