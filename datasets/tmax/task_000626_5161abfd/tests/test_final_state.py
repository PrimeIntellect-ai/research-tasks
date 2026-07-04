# test_final_state.py

import os
import subprocess
import pytest

def test_run_etl_script_exists_and_executable():
    script_path = '/home/user/run_etl.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_crontab_entry_exists():
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Has it been set up?")

    # Look for the specific cron schedule and script
    found = False
    for line in crontab_content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '*/15 * * * *' in line and '/home/user/run_etl.sh' in line:
            found = True
            break

    assert found, "Crontab entry for /home/user/run_etl.sh running every 15 minutes was not found."

def test_merged_csv_output():
    output_path = '/home/user/output/merged.csv'
    assert os.path.isfile(output_path), f"{output_path} does not exist. Did the ETL pipeline run?"

    expected_content = (
        "timestamp,temperature,humidity\n"
        "1697107200,22.4,45.2\n"
        "1697107500,22.5,46.1\n"
        "1697107800,22.6,45.8\n"
        "1697108700,23.4,48.5\n"
    )

    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            actual_content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"{output_path} is not properly encoded in UTF-8.")

    # Normalize line endings and strip whitespace
    actual_lines = [line.strip() for line in actual_content.strip().splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {output_path} does not match the expected inner join result.\n"
        f"Expected:\n{expected_lines}\nActual:\n{actual_lines}"
    )

def test_etl_cpp_exists():
    cpp_path = '/home/user/etl.cpp'
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."