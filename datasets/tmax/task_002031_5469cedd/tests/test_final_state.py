# test_final_state.py

import os
import json
import stat

def test_cpp_source_exists():
    path = "/home/user/deadlock_detector.cpp"
    assert os.path.exists(path), f"C++ source file {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_compiled_detector_exists_and_executable():
    path = "/home/user/detector"
    assert os.path.exists(path), f"Compiled executable {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_process_sh_exists_and_executable():
    path = "/home/user/process.sh"
    assert os.path.exists(path), f"Bash script {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_deadlock_report_json():
    path = "/home/user/deadlock_report.json"
    assert os.path.exists(path), f"Report file {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    assert "deadlock_detected" in data, "Key 'deadlock_detected' missing from JSON."
    assert data["deadlock_detected"] is True, "Expected 'deadlock_detected' to be true."

    assert "deadlocked_transactions" in data, "Key 'deadlocked_transactions' missing from JSON."
    txs = data["deadlocked_transactions"]
    assert isinstance(txs, list), "'deadlocked_transactions' should be a list."

    expected_txs = ["Tx11", "Tx12", "Tx13"]
    assert sorted(txs) == expected_txs, f"Expected deadlocked_transactions to be {expected_txs}, but got {sorted(txs)}."