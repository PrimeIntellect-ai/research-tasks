# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_secure_audit_permissions():
    """
    Validates that the secure_audit directory and audit.enc file
    have the strictly required permissions (0700 and 0600 respectively).
    """
    audit_dir = "/home/user/secure_audit"
    audit_file = "/home/user/secure_audit/audit.enc"

    assert os.path.isdir(audit_dir), f"Expected directory {audit_dir} is missing."
    dir_stat = os.stat(audit_dir)
    dir_perms = stat.S_IMODE(dir_stat.st_mode)
    assert dir_perms == 0o700, f"Directory {audit_dir} must have 0700 permissions, but has {oct(dir_perms)}."

    assert os.path.isfile(audit_file), f"Expected file {audit_file} is missing."
    file_stat = os.stat(audit_file)
    file_perms = stat.S_IMODE(file_stat.st_mode)
    assert file_perms == 0o600, f"File {audit_file} must have 0600 permissions, but has {oct(file_perms)}."

def test_audit_file_structure():
    """
    Validates the structure of the encrypted audit file.
    It must consist of concatenated records, each prefixed by a 2-byte big-endian length.
    """
    audit_file = "/home/user/secure_audit/audit.enc"
    assert os.path.isfile(audit_file), f"File {audit_file} does not exist."

    with open(audit_file, "rb") as f:
        data = f.read()

    assert len(data) > 0, f"File {audit_file} is empty."

    offset = 0
    record_count = 0
    while offset < len(data):
        if offset + 2 > len(data):
            pytest.fail(f"Incomplete 2-byte length header at offset {offset} in {audit_file}.")

        length = int.from_bytes(data[offset:offset+2], byteorder='big')
        offset += 2

        if offset + length > len(data):
            pytest.fail(f"Record length {length} at offset {offset-2} exceeds remaining file size.")

        offset += length
        record_count += 1

    assert record_count > 0, f"No valid encrypted records found in {audit_file}."

def test_f1_score_metric():
    """
    Uses the provided verifier tool to compute the F1 score of the malicious line detection.
    Asserts that the F1 score meets or exceeds the threshold of 0.95.
    """
    verify_script = "/app/verify.py"
    assert os.path.isfile(verify_script), f"Verifier script {verify_script} not found."

    # Run the verifier script
    result = subprocess.run(["python3", verify_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Verifier script failed to run. Stderr: {result.stderr}"

    output = result.stdout.strip()

    # Extract the F1 score from the verifier's output
    # Look for a floating point number in the output
    matches = re.findall(r"0\.\d+|1\.0+", output)
    if not matches:
        try:
            score = float(output)
        except ValueError:
            pytest.fail(f"Could not parse a valid F1 score from verifier output: '{output}'")
    else:
        score = float(matches[-1])

    threshold = 0.95
    assert score >= threshold, f"F1 score {score} is below the required threshold of {threshold}."