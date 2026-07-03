# test_final_state.py

import os
import subprocess
import random
import pytest

def test_recovered_database():
    sql_path = "/home/user/recovered.sql"
    assert os.path.exists(sql_path), f"Missing recovered SQL dump at {sql_path}"

    with open(sql_path, "r") as f:
        content = f.read()

    assert "audio_metadata" in content, "Recovered SQL does not contain 'audio_metadata' table."
    assert "0.005" in content, "Recovered SQL does not contain the expected threshold value (0.005)."

def test_fuzz_equivalence():
    agent_script = "/home/user/recreated_processor.sh"
    oracle_binary = "/app/oracle_processor"

    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"
    assert os.path.exists(oracle_binary), f"Oracle binary missing at {oracle_binary}"

    random.seed(42)

    for _ in range(1000):
        freq = random.uniform(100.0, 5000.0)
        threshold = random.uniform(0.0001, 10.0)

        # Randomly format inputs to include normal floats, scientific notation, and extra spaces
        fmt_choice_freq = random.choice([0, 1, 2])
        if fmt_choice_freq == 0:
            freq_str = f"{freq:.4f}"
        elif fmt_choice_freq == 1:
            freq_str = f"{freq:.4e}"
        else:
            freq_str = f"  {freq:.4f}  "

        fmt_choice_thresh = random.choice([0, 1, 2])
        if fmt_choice_thresh == 0:
            thresh_str = f"{threshold:.4f}"
        elif fmt_choice_thresh == 1:
            thresh_str = f"{threshold:.4e}"
        else:
            thresh_str = f"  {threshold:.4f}  "

        # Run oracle
        try:
            oracle_out = subprocess.check_output([oracle_binary, freq_str, thresh_str], text=True).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on inputs '{freq_str}', '{thresh_str}': {e}")

        # Run agent script
        try:
            agent_out = subprocess.check_output(["bash", agent_script, freq_str, thresh_str], text=True).strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on inputs '{freq_str}', '{thresh_str}': {e}")

        assert oracle_out == agent_out, (
            f"Mismatch on inputs freq='{freq_str}', threshold='{thresh_str}'. "
            f"Oracle: '{oracle_out}', Agent: '{agent_out}'"
        )