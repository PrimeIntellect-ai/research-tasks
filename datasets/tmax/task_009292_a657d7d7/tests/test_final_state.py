# test_final_state.py
import os
import gzip
import stat

def test_ci_logger_compiled():
    path = "/home/user/ci_logger"
    assert os.path.isfile(path), f"Executable {path} not found. Did you compile the C++ code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_run_ci_script():
    path = "/home/user/run_ci.sh"
    assert os.path.isfile(path), f"Script {path} not found."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

    with open(path, "r") as f:
        content = f.read()

    # Check for robust error handling
    assert "set -e" in content or "set -o errexit" in content or "set -o pipefail" in content, \
        "Script does not appear to enable robust error handling (e.g., set -e or set -o pipefail)."

def test_logrotate_conf():
    path = "/home/user/logrotate.conf"
    assert os.path.isfile(path), f"logrotate configuration {path} not found."

    with open(path, "r") as f:
        content = f.read()

    assert "/home/user/logs/ci_build.log" in content, "logrotate.conf does not target /home/user/logs/ci_build.log"
    assert "daily" in content, "logrotate.conf missing 'daily' rule"
    assert "rotate 3" in content, "logrotate.conf missing 'rotate 3' rule"
    assert "compress" in content, "logrotate.conf missing 'compress' rule"
    assert "missingok" in content, "logrotate.conf missing 'missingok' rule"

def test_logrotate_output():
    log_gz = "/home/user/logs/ci_build.log.1.gz"
    assert os.path.isfile(log_gz), f"Rotated log file {log_gz} not found. Did you run logrotate?"

    expected_lines = [
        "[CI] Build initialized",
        "[CI] FATAL: Missing provisioning credentials",
        "[CI] Build process terminated early"
    ]

    with gzip.open(log_gz, "rt") as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, \
        f"The content of the rotated log does not match the expected processed output. Got: {content}"