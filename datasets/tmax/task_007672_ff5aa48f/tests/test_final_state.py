# test_final_state.py

import os

def test_results_txt_content():
    results_file = '/home/user/results.txt'
    assert os.path.exists(results_file), f"{results_file} not found. The script did not generate the output file."

    with open(results_file, 'r') as f:
        content = f.read().strip()

    assert "Trace: 29.83" in content, f"Incorrect trace in results.txt. Expected 'Trace: 29.83', got:\n{content}"
    assert "Mean_Prediction: 11.75" in content, f"Incorrect mean prediction in results.txt. Expected 'Mean_Prediction: 11.75', got:\n{content}"

def test_etl_script_exists():
    script_file = '/home/user/etl_test.py'
    assert os.path.exists(script_file), f"{script_file} not found. You must write the ETL script to this location."