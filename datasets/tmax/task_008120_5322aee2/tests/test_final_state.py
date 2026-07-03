# test_final_state.py
import os
import pytest

def test_decrypted_evidence_exists_and_correct():
    """Verify that the student successfully decrypted the payload and wrote the flag."""
    evidence_path = "/home/user/decrypted_evidence.txt"

    assert os.path.isfile(evidence_path), f"The final evidence file is missing: {evidence_path}"

    with open(evidence_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{P4th_Tr4v3rs4l_C3rt_GCM_M4st3r}"
    assert content == expected_flag, (
        f"The decrypted payload does not match the expected flag.\n"
        f"Expected: {expected_flag}\n"
        f"Found: {content}"
    )