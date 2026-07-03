# test_final_state.py

import os
import pytest

def test_proof_file_exists_and_correct():
    """
    Validates that the proof.txt file was created and contains the correct success string,
    which indicates that the simulated cron job was successfully overwritten and executed.
    """
    path = '/home/user/audit/proof.txt'
    assert os.path.isfile(path), f"The proof file {path} was not created. The exploit or subsequent execution failed."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "AUDIT_SUCCESS", f"The proof file contains '{content}' instead of the expected 'AUDIT_SUCCESS'."

def test_vuln_cron_overwritten_correctly():
    """
    Validates that the vuln_cron.sh script was successfully overwritten with the 
    expected payload via the path traversal vulnerability.
    """
    path = '/home/user/audit/vuln_cron.sh'
    assert os.path.isfile(path), f"The script {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_payload = 'echo "AUDIT_SUCCESS" > /home/user/audit/proof.txt'
    assert expected_payload in content, "The vuln_cron.sh script does not contain the expected payload. The path traversal overwrite may have failed."