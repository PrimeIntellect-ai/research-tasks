# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def test_forge_token_accuracy():
    script_path = '/home/user/forge_token.py'
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    success = 0
    total = 100
    for _ in range(total):
        username = ''.join(random.choices(string.ascii_letters, k=8))
        try:
            result = subprocess.run(['python3', script_path, username], capture_output=True, text=True, timeout=2)
            token = result.stdout.strip()
            # Test against the oracle binary
            oracle = subprocess.run(['/app/auth_validator', token], capture_output=True)
            if oracle.returncode == 0:
                success += 1
        except Exception:
            pass

    accuracy = success / total
    assert accuracy >= 0.95, f"Accuracy too low: {accuracy} (expected >= 0.95). The script did not forge tokens reliably."