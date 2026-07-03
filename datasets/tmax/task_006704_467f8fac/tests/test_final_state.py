# test_final_state.py
import os
import pytest

def test_verified_deps_output():
    output_path = '/home/user/verified_deps.txt'
    assert os.path.isfile(output_path), f"{output_path} does not exist. The task requires writing valid dependencies to this file."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "click==8.0.0",
        "flask==1.1.2",
        "requests==2.25.1",
        "urllib3==1.26.4"
    ]

    assert lines == expected, f"Content of {output_path} is incorrect. Expected {expected}, got {lines}."