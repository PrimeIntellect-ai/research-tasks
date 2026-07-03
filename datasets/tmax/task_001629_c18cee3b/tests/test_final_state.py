# test_final_state.py

import os
import re
import math
import subprocess
import pytest

def get_expected_payload():
    dump_path = "/home/user/metrics/mem.dump"
    assert os.path.isfile(dump_path), f"Missing {dump_path}"

    with open(dump_path, "rb") as f:
        content = f.read().decode('utf-8', errors='ignore')

    match = re.search(r"\[CRASH_CONTEXT\] LAST_BUFFER:\s+(.*?)\s+\[/CRASH_CONTEXT\]", content)
    assert match is not None, "Could not find crash context in mem.dump"

    numbers_str = match.group(1)
    numbers = [int(x) for x in numbers_str.strip().split()]
    return numbers

def test_payload_extracted():
    payload_path = "/home/user/solution/payload.txt"
    assert os.path.isfile(payload_path), f"{payload_path} does not exist."

    expected_numbers = get_expected_payload()

    with open(payload_path, "r") as f:
        lines = f.read().strip().splitlines()

    actual_numbers = [int(x.strip()) for x in lines if x.strip()]

    assert actual_numbers == expected_numbers, f"Payload numbers in {payload_path} do not match the expected numbers from mem.dump."

def test_mre_script():
    mre_path = "/home/user/solution/mre.sh"
    assert os.path.isfile(mre_path), f"{mre_path} does not exist."
    assert os.access(mre_path, os.X_OK), f"{mre_path} is not executable."

    with open(mre_path, "r") as f:
        content = f.read()

    assert "awk" in content, f"{mre_path} does not contain an awk command."

    # Run the mre script and check its stderr
    result = subprocess.run([mre_path], capture_output=True, text=True, cwd="/home/user/solution")

    stderr_output = result.stderr
    assert "awk:" in stderr_output and "sqrt: called with negative argument" in stderr_output, \
        f"{mre_path} did not produce the expected awk catastrophic cancellation warning on stderr. Stderr was: {stderr_output}"

def test_calculated_answer():
    answer_path = "/home/user/solution/answer.txt"
    assert os.path.isfile(answer_path), f"{answer_path} does not exist."

    expected_numbers = get_expected_payload()

    # Calculate correct standard deviation
    n = len(expected_numbers)
    assert n > 0, "No numbers found to calculate standard deviation."

    mean = sum(expected_numbers) / n
    variance = sum((x - mean) ** 2 for x in expected_numbers) / n
    stddev = math.sqrt(variance)

    expected_answer = f"{stddev:.4f}"

    with open(answer_path, "r") as f:
        actual_answer = f.read().strip()

    assert actual_answer == expected_answer, f"Expected answer {expected_answer}, but got {actual_answer} in {answer_path}."