# test_final_state.py
import os
import re
import pytest

def test_generate_data_script_exists():
    assert os.path.exists('/home/user/generate_data.py'), "generate_data.py is missing"

def test_test_generator_script_exists():
    assert os.path.exists('/home/user/test_generator.py'), "test_generator.py is missing"
    with open('/home/user/test_generator.py', 'r') as f:
        content = f.read()
        assert 'pytest' in content or 'test' in content, "test_generator.py does not look like a test script"
        assert '0.05' in content, "test_generator.py does not check for the 0.05 tolerance"

def test_synthetic_data_csv():
    csv_path = '/home/user/synthetic_data.csv'
    assert os.path.exists(csv_path), "synthetic_data.csv is missing"

    with open(csv_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 100001, f"Expected 100001 lines in synthetic_data.csv, found {len(lines)}"
    assert lines[0].strip() == 'f1,f2,f3', f"Expected header 'f1,f2,f3', found '{lines[0].strip()}'"

    # Check that the first data row has 3 columns and looks like floats
    first_data = lines[1].strip().split(',')
    assert len(first_data) == 3, "Data rows should have 3 columns"
    try:
        [float(x) for x in first_data]
    except ValueError:
        pytest.fail("Data rows do not contain valid floats")

def test_test_results_log():
    log_path = '/home/user/test_results.log'
    assert os.path.exists(log_path), "test_results.log is missing"

    with open(log_path, 'r') as f:
        content = f.read().lower()

    assert 'passed' in content or 'pass' in content, "test_results.log does not indicate a passing test"
    assert 'failed' not in content, "test_results.log indicates a failing test"