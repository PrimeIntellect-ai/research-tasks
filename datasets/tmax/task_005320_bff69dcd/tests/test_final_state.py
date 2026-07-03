# test_final_state.py
import os
import subprocess
import pytest

def test_filter_clean_corpus():
    script_path = "/home/user/filter.py"
    assert os.path.exists(script_path), f"Missing script at {script_path}"

    clean_dir = "/app/corpus/clean"
    assert os.path.exists(clean_dir), f"Missing directory {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    assert len(clean_files) > 0, f"No CSV files found in {clean_dir}"

    failed_files = []
    for csv_file in clean_files:
        result = subprocess.run(["python3", script_path, csv_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "clean":
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (expected 'clean', got something else). Offending files: {', '.join(failed_files[:10])}")

def test_filter_evil_corpus():
    script_path = "/home/user/filter.py"
    assert os.path.exists(script_path), f"Missing script at {script_path}"

    evil_dir = "/app/corpus/evil"
    assert os.path.exists(evil_dir), f"Missing directory {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]
    assert len(evil_files) > 0, f"No CSV files found in {evil_dir}"

    failed_files = []
    for csv_file in evil_files:
        result = subprocess.run(["python3", script_path, csv_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "evil":
            failed_files.append(os.path.basename(csv_file))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (expected 'evil', got something else). Offending files: {', '.join(failed_files[:10])}")

def test_plot_data_fixed():
    script_path = "/home/user/plot_data.py"
    assert os.path.exists(script_path), f"Missing script at {script_path}"

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"plot_data.py failed to run. It may still have the matplotlib backend issue. Error: {result.stderr}"