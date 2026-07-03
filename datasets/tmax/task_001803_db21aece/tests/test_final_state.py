# test_final_state.py

import os
import subprocess
import pytest

def test_ticket_output():
    path = "/home/user/ticket_4492_output.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "alice,bob", f"Expected 'alice,bob' in {path}, but got '{content}'"

def test_mre_script():
    path = "/home/user/mre.py"
    assert os.path.isfile(path), f"File {path} is missing."

    result = subprocess.run(["python3", path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} failed to execute."

    output = result.stdout.strip()
    assert output == "False", f"Expected mre.py to output 'False', but got '{output}'"

def test_fuzz_log():
    path = "/home/user/fuzz.log"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "FUZZ_OK", f"Expected 'FUZZ_OK' in {path}, but got '{content}'"

def test_billing_query_uses_decimal():
    path = "/home/user/billing_query.py"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "decimal" in content, f"Expected 'decimal' to be imported and used in {path}"