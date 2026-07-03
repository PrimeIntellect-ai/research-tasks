# test_final_state.py

import os
import subprocess
import random
import pytest

def generate_text():
    words = ["cat", "dog", "bird", "fish", "apple", "tree", "car", "house", "Cat!", "DOG.", "bIrD?"]
    return " ".join(random.choices(words, k=50))

def test_score_script_mse():
    script_path = "/home/user/score.sh"
    oracle_path = "/app/score_oracle"

    assert os.path.exists(script_path), f"User script not found at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

    mse = 0.0
    n = 20
    random.seed(42) # For reproducibility

    for i in range(n):
        test_file = f"/tmp/test_{i}.txt"
        with open(test_file, "w") as f:
            f.write(generate_text())

        try:
            oracle_out = subprocess.check_output([oracle_path, test_file], text=True).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on {test_file}: {e}")

        try:
            agent_out = subprocess.check_output(["bash", script_path, test_file], text=True).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"User script failed on {test_file}: {e}")

        try:
            oracle_val = float(oracle_out)
        except ValueError:
            pytest.fail(f"Oracle output is not a float: {oracle_out}")

        try:
            agent_val = float(agent_out)
        except ValueError:
            pytest.fail(f"User script output is not a float: {agent_out}")

        diff = oracle_val - agent_val
        mse += diff * diff

    mse /= n

    threshold = 0.05
    assert mse <= threshold, f"MSE {mse:.5f} exceeds the threshold of {threshold}"