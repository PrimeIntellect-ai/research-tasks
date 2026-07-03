# test_final_state.py
import os
import subprocess
import pytest
from decimal import Decimal

def test_output_txt_content():
    data_path = '/home/user/data.txt'
    output_path = '/home/user/output.txt'

    assert os.path.exists(data_path), f"Data file missing: {data_path}"
    assert os.path.exists(output_path), f"Output file missing: {output_path}"

    # Calculate expected sum using Decimal to avoid floating point issues
    expected_sum = Decimal('0.0')
    with open(data_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                expected_sum += Decimal(line)

    expected_str = str(expected_sum)

    with open(output_path, 'r') as f:
        output_content = f.read().strip()

    assert output_content == expected_str, f"Expected output {expected_str}, but got '{output_content}'. Make sure both the off-by-one error and floating-point precision issues are fixed."

def test_requirements_installed():
    # Check if requests can be imported successfully (which implies urllib3 is compatible)
    try:
        subprocess.run(
            ['python3', '-c', 'import requests'],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to import requests. Dependency conflict might not be resolved. Error: {e.stderr}")