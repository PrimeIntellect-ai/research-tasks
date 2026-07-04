# test_final_state.py
import os
import json
import csv

def test_script_exists():
    assert os.path.exists('/home/user/generate_data.py'), "Script /home/user/generate_data.py not found"

def test_plot_exists():
    assert os.path.exists('/home/user/oscillator_plot.png'), "Plot /home/user/oscillator_plot.png not found"

def test_csv_output():
    csv_path = '/home/user/training_data.csv'
    assert os.path.exists(csv_path), f"CSV file {csv_path} not found"

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_columns = ['t', 'x_num', 'v_num', 'x_ana', 'v_ana']
        assert header == expected_columns, f"CSV columns incorrect. Expected {expected_columns}, got {header}"

        rows = list(reader)
        assert len(rows) == 1000, f"CSV length incorrect. Expected 1000 rows, got {len(rows)}"

def test_json_report():
    json_path = '/home/user/training_data_report.json'
    assert os.path.exists(json_path), f"JSON file {json_path} not found"

    with open(json_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, "JSON file is not valid"

    assert 'mse_x' in report, "Key 'mse_x' missing in JSON report"
    assert 'mse_v' in report, "Key 'mse_v' missing in JSON report"

    mse_x = report['mse_x']
    mse_v = report['mse_v']

    assert isinstance(mse_x, (int, float)), "mse_x must be a number"
    assert isinstance(mse_v, (int, float)), "mse_v must be a number"

    assert mse_x < 1e-4, f"mse_x too high: {mse_x}. Expected < 1e-4"
    assert mse_v < 1e-2, f"mse_v too high: {mse_v}. Expected < 1e-2"