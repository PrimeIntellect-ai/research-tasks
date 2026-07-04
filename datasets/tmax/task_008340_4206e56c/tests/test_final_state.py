# test_final_state.py
import os

def test_crash_tx_txt():
    path = "/home/user/crash_tx.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you extract the transaction ID?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "TX-99382-ALPHA", f"Expected 'TX-99382-ALPHA' in {path}, but got '{content}'"

def test_runner_sh_fixed():
    path = "/home/user/legacy_app/runner.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()

    # The user must have exported or set BYPASS_LEGACY_LOCKS in the script
    assert "BYPASS_LEGACY_LOCKS" in content, f"The required environment variable bypass was not found in {path}."

def test_total_value_txt():
    path = "/home/user/total_value.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you calculate the sum and save it?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "500", f"Expected '500' in {path}, but got '{content}'"