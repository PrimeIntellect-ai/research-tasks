# test_final_state.py
import os
import json
import sqlite3
import base64
import statistics

def test_hidden_output_dir_exists():
    dir_path = "/home/user/hidden_output_dir"
    assert os.path.exists(dir_path), f"Directory {dir_path} does not exist."
    assert os.path.isdir(dir_path), f"{dir_path} is not a directory."

def test_metrics_out_json_exists():
    file_path = "/home/user/hidden_output_dir/metrics_out.json"
    assert os.path.exists(file_path), f"File {file_path} does not exist. The script probably didn't run successfully or write the output."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{file_path} does not contain valid JSON."

    assert "temperature_variance" in data, f"'temperature_variance' key missing from {file_path}."

def test_final_answer_txt_correct():
    file_path = "/home/user/final_answer.txt"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    # Recompute expected values from the database to be robust
    db_path = "/home/user/metrics.db"
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT payload FROM sensor_data')

    temps = []
    for row in c.fetchall():
        payload_raw = row[0]
        try:
            json_str = base64.b64decode(payload_raw).decode('utf-8')
            data = json.loads(json_str)
            temps.append(data['temperature'])
        except Exception:
            pass
    conn.close()

    assert len(temps) > 0, "Could not extract temperatures from the database."

    expected_pvariance = statistics.pvariance(temps)
    expected_variance = statistics.variance(temps)

    expected_pvar_str = f"{expected_pvariance:.4f}"
    expected_var_str = f"{expected_variance:.4f}"

    assert content in [expected_pvar_str, expected_var_str], \
        f"Expected {file_path} to contain {expected_pvar_str} or {expected_var_str}, but got '{content}'."