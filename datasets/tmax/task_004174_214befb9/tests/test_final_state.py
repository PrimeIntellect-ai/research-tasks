# test_final_state.py
import os
import re

def test_scripts_exist_and_executable():
    parse_logs = "/home/user/parse_logs.sh"
    run_sandbox = "/home/user/run_sandbox.sh"

    assert os.path.isfile(parse_logs), f"Expected script {parse_logs} does not exist."
    assert os.path.isfile(run_sandbox), f"Expected script {run_sandbox} does not exist."

    # Check if executable (optional but good practice for bash scripts)
    assert os.access(parse_logs, os.X_OK), f"{parse_logs} is not executable."
    assert os.access(run_sandbox, os.X_OK), f"{run_sandbox} is not executable."

def test_run_sandbox_content():
    run_sandbox = "/home/user/run_sandbox.sh"
    with open(run_sandbox, "r") as f:
        content = f.read()

    assert "bwrap" in content, "run_sandbox.sh must use bwrap."
    assert "--ro-bind" in content, "run_sandbox.sh must use --ro-bind to mount / read-only."
    assert "--bind" in content, "run_sandbox.sh must use --bind to mount the output directory."
    assert "--unshare-all" in content, "run_sandbox.sh must use --unshare-all."

def test_redacted_failed_log_content():
    output_file = "/home/user/output/redacted_failed.log"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did you run the sandbox script?"

    with open(output_file, "r") as f:
        content = f.read().strip().split('\n')

    expected_content = [
        "2023-11-01T08:15:22 INFO [api.legacy-system.net] Initializing connection for user=admin cc=XXXX-XXXX-XXXX-XXXX",
        "2023-11-01T08:15:23 ERROR [api.legacy-system.net] CERT_CHAIN_FAIL Expired certificate in chain",
        "2023-11-01T08:15:25 INFO [api.legacy-system.net] Retrying connection without tls...",
        "2023-11-01T08:20:01 INFO [analytics.tracker.io] Data sync cc=XXXX-XXXX-XXXX-XXXX",
        "2023-11-01T08:20:02 ERROR [analytics.tracker.io] CERT_CHAIN_FAIL Self-signed cert"
    ]

    assert len(content) == len(expected_content), f"Expected {len(expected_content)} lines in {output_file}, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_content)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_no_unredacted_cc_numbers():
    output_file = "/home/user/output/redacted_failed.log"
    if not os.path.isfile(output_file):
        return # Handled by previous test

    with open(output_file, "r") as f:
        content = f.read()

    # Pattern for unredacted credit card numbers
    cc_pattern = re.compile(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b')
    unredacted = cc_pattern.findall(content)

    assert len(unredacted) == 0, f"Found unredacted credit card numbers in the output: {unredacted}"