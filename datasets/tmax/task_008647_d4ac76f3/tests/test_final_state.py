# test_final_state.py

import os
import subprocess
import pytest

BUG_REPORT = "/home/user/bug_report.txt"
PIPELINE_OUTPUT = "/home/user/pipeline_output.txt"
PIPELINE_DIR = "/home/user/pipeline"
PARSER_PY = os.path.join(PIPELINE_DIR, "parser.py")
LARGE_INPUT = os.path.join(PIPELINE_DIR, "large_input.txt")
EXPECTED_MALFORMED_LINE = "2023-10-14 10:22:14 [WARN] Connection timeout <data>partial_payload_missing_closing_tag"

def test_bug_report_content():
    assert os.path.isfile(BUG_REPORT), f"{BUG_REPORT} does not exist."
    with open(BUG_REPORT, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_MALFORMED_LINE, f"{BUG_REPORT} does not contain the correct isolated log line."

def test_parser_loop_termination():
    assert os.path.isfile(PARSER_PY), f"{PARSER_PY} does not exist."

    # Test if the script hangs on the malformed line
    try:
        process = subprocess.run(
            ["python3", PARSER_PY],
            input=EXPECTED_MALFORMED_LINE + "\n",
            capture_output=True,
            text=True,
            timeout=2.0
        )
        # If it completes within 2 seconds, the infinite loop is fixed
        assert process.returncode == 0, "parser.py crashed or returned non-zero exit code."
    except subprocess.TimeoutExpired:
        pytest.fail("parser.py still hangs on the malformed input line (infinite loop not fixed).")

def test_pipeline_output_correctness():
    assert os.path.isfile(LARGE_INPUT), f"{LARGE_INPUT} does not exist."
    assert os.path.isfile(PIPELINE_OUTPUT), f"{PIPELINE_OUTPUT} does not exist."

    # Compute expected output
    expected_payloads = []
    with open(LARGE_INPUT, "r") as f:
        for line in f:
            line = line.strip()
            remain = line
            while "<data>" in remain:
                start = remain.find("<data>") + 6
                end = remain.find("</data>", start)
                if end != -1:
                    expected_payloads.append(remain[start:end])
                    remain = remain[end+7:]
                else:
                    break

    # Read actual output
    with open(PIPELINE_OUTPUT, "r") as f:
        actual_payloads = [line.strip() for line in f if line.strip()]

    assert len(actual_payloads) == len(expected_payloads), f"Expected {len(expected_payloads)} payloads, but found {len(actual_payloads)} in {PIPELINE_OUTPUT}."
    assert actual_payloads == expected_payloads, f"The contents of {PIPELINE_OUTPUT} do not match the expected extracted data payloads."