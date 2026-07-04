# test_final_state.py
import os
import pandas as pd
import pytest

def test_etl_cpp_exists():
    assert os.path.isfile('/home/user/etl.cpp'), "/home/user/etl.cpp is missing"

def test_etl_bin_exists():
    assert os.path.isfile('/home/user/etl_bin'), "/home/user/etl_bin is missing"
    assert os.access('/home/user/etl_bin', os.X_OK), "/home/user/etl_bin is not executable"

def test_summary_csv_exists():
    assert os.path.isfile('/home/user/summary.csv'), "/home/user/summary.csv is missing"

def test_summary_csv_metric():
    csv_path = '/home/user/summary.csv'
    assert os.path.isfile(csv_path), f"{csv_path} is missing"

    try:
        agent_df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path}: {e}")

    assert 'session_id' in agent_df.columns, "Column 'session_id' missing in summary.csv"
    assert 'total_amount' in agent_df.columns, "Column 'total_amount' missing in summary.csv"

    try:
        agent_df['total_amount'] = agent_df['total_amount'].astype(float).round(2)
    except Exception as e:
        pytest.fail(f"Failed to convert total_amount to float: {e}")

    expected = {101: 50.00, 102: 100.00, 103: 100.00}

    correct = 0
    for _, row in agent_df.iterrows():
        try:
            sid = int(row['session_id'])
            amt = float(row['total_amount'])
            if sid in expected and abs(expected[sid] - amt) < 0.01:
                correct += 1
        except ValueError:
            continue

    precision = correct / len(agent_df) if len(agent_df) > 0 else 0
    recall = correct / len(expected)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 1.0, f"F1 Score is {f1:.2f}, expected >= 1.0"