# test_final_state.py
import os
import json
import subprocess

def test_input_json_extracted():
    path = "/home/user/input.json"
    assert os.path.isfile(path), f"File {path} does not exist. Payload was not extracted."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{path} does not contain valid JSON."

    assert "expected_total" in data, "Extracted JSON is missing 'expected_total'."
    assert "transactions" in data, "Extracted JSON is missing 'transactions'."
    assert str(data["expected_total"]) == "10000000000000000.05", "Extracted JSON has incorrect 'expected_total'."

def test_bad_tx_identified():
    path = "/home/user/bad_tx.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Bad transaction not identified."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "tx_giant_bug", f"Incorrect transaction ID in {path}: expected 'tx_giant_bug', got '{content}'."

def test_total_txt_correct():
    path = "/home/user/total.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Fixed script did not write the total."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "10000000000000000.05", f"Incorrect total in {path}: expected '10000000000000000.05', got '{content}'."

def test_billing_py_uses_decimal():
    path = "/home/user/billing.py"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "decimal" in content.lower(), "The script billing.py does not appear to use the 'decimal' module as required."

def test_billing_py_execution():
    script_path = "/home/user/billing.py"
    input_path = "/home/user/input.json"

    # Ensure input.json exists before running
    if not os.path.isfile(input_path):
        assert False, f"Cannot test execution because {input_path} is missing."

    result = subprocess.run(
        ["python3", script_path, input_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"billing.py failed to execute successfully.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"