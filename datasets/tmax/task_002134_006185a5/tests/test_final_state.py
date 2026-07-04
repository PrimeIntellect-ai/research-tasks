# test_final_state.py

import os
import glob
import shutil
import tempfile
import subprocess
import csv
import pytest

def test_classifier_script():
    # 1. Find the agent's script
    possible_scripts = glob.glob("/home/user/classify.*")
    assert possible_scripts, "No classify script found at /home/user/classify.*"

    # Prefer .py, .sh, .js in that order, or just take the first one
    script_path = possible_scripts[0]

    # 2. Setup combined corpus directory
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(clean_dir), f"Clean corpus missing at {clean_dir}"
    assert os.path.exists(evil_dir), f"Evil corpus missing at {evil_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]

    with tempfile.TemporaryDirectory() as tmp_input_dir:
        for f in clean_files:
            shutil.copy(os.path.join(clean_dir, f), os.path.join(tmp_input_dir, f))
        for f in evil_files:
            shutil.copy(os.path.join(evil_dir, f), os.path.join(tmp_input_dir, f))

        output_csv = os.path.join(tmp_input_dir, "results.csv")

        # 3. Run the agent's script
        # If it's a python file and not executable, we might need to run `python script.py`
        cmd = []
        if script_path.endswith('.py') and not os.access(script_path, os.X_OK):
            cmd = ["python3", script_path]
        elif script_path.endswith('.js') and not os.access(script_path, os.X_OK):
            cmd = ["node", script_path]
        else:
            cmd = [script_path]

        cmd.extend([tmp_input_dir, output_csv])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except Exception as e:
            pytest.fail(f"Failed to execute the classification script: {e}")

        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        assert os.path.exists(output_csv), f"Output CSV not found at {output_csv}"

        # 4. Parse the output CSV
        results = {}
        with open(output_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            assert header == ['filename', 'status'], f"Expected CSV header ['filename', 'status'], got {header}"

            for row in reader:
                if len(row) == 2:
                    results[row[0]] = row[1].strip().lower()

        # 5. Verify results
        clean_failures = []
        evil_failures = []

        for f in clean_files:
            if results.get(f) != 'clean':
                clean_failures.append(f)

        for f in evil_files:
            if results.get(f) != 'evil':
                evil_failures.append(f)

        error_msg = []
        if clean_failures:
            error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures[:5])}{'...' if len(clean_failures) > 5 else ''}")
        if evil_failures:
            error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures[:5])}{'...' if len(evil_failures) > 5 else ''}")

        if error_msg:
            pytest.fail(" | ".join(error_msg))