# test_final_state.py
import os
import pytest

def test_recover_c_exists():
    path = "/home/user/investigation/recover.c"
    assert os.path.isfile(path), f"The C program was not found at {path}"

def test_recovered_evidence_content():
    path = "/home/user/recovered_evidence.txt"
    assert os.path.isfile(path), f"The recovered evidence file was not found at {path}"

    expected_evidence = "EVIDENCE{path_traversal_and_brute_force_master_9921}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected_evidence, f"The content of {path} is incorrect. Expected '{expected_evidence}', but got '{content}'"