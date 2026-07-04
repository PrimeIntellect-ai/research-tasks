# test_final_state.py

import os
import subprocess
import pytest

def test_crash_payload_file():
    payload_file = "/home/user/crash_payload.txt"
    assert os.path.isfile(payload_file), f"File {payload_file} does not exist."

    with open(payload_file, "r") as f:
        content = f.read().strip()

    expected_payload = "0301f10a0b0c0d0e"
    assert content == expected_payload, f"Expected crash payload '{expected_payload}', but got '{content}'"

def test_parser_go_fixed():
    parser_file = "/home/user/project/parser.go"
    assert os.path.isfile(parser_file), f"File {parser_file} does not exist."

    with open(parser_file, "r") as f:
        content = f.read()

    # The instructions specifically ask to return errors.New("invalid length")
    assert "invalid length" in content, "The error message 'invalid length' was not found in parser.go"

def test_go_fuzz_tests_pass():
    project_dir = "/home/user/project"
    assert os.path.isdir(project_dir), f"Directory {project_dir} does not exist."

    try:
        result = subprocess.run(
            ["go", "test", "-fuzz=FuzzParsePacket", "-fuzztime=2s"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Go fuzz tests timed out after 30 seconds.")
    except FileNotFoundError:
        pytest.fail("The 'go' command was not found.")

    assert result.returncode == 0, f"Go fuzz tests failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert "ok" in result.stdout or "PASS" in result.stdout, "Fuzz tests did not output 'ok' or 'PASS'."