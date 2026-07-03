# test_final_state.py

import os
import subprocess
import pytest

def test_recovered_data_csv():
    path = "/home/user/recovered_data.csv"
    assert os.path.isfile(path), f"File {path} does not exist. Did you recover the deleted file?"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1000, f"Expected 1000 lines in {path}, found {len(lines)}"

    count_10 = lines.count("10")
    count_neg1 = lines.count("-1")

    assert count_10 == 999, f"Expected 999 occurrences of '10' in {path}, found {count_10}"
    assert count_neg1 == 1, f"Expected 1 occurrence of '-1' in {path}, found {count_neg1}"

def test_summary_report_txt():
    path = "/home/user/summary_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the script and redirect output?"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "10: 999", f"Expected summary report to contain exactly '10: 999', but found: '{content}'"

def test_process_data_script_fixed():
    script_path = "/home/user/data_pipeline/process_data.sh"
    data_path = "/home/user/recovered_data.csv"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    try:
        result = subprocess.run([script_path, data_path], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        assert output == "10: 999", f"Expected script output to be '10: 999', but got: '{output}'"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script crashed or returned non-zero exit code when run on recovered data. Error: {e.stderr}")