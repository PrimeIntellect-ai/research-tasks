# test_final_state.py
import os

def test_success_log_exists_and_content():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. The exploit may not have succeeded or was not executed."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "pwned", f"The file {log_path} does not contain the exact word 'pwned'. Found: {content!r}"

def test_exploit_script_exists():
    exploit_path = "/home/user/exploit.py"
    assert os.path.isfile(exploit_path), f"The exploit script {exploit_path} does not exist. Did you create it as requested?"