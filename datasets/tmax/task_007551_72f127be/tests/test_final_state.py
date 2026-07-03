# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

def test_etl_scripts_exist():
    """Verify that the Python script and Bash wrapper exist, and the wrapper is executable."""
    assert os.path.isfile('/home/user/etl_pipeline.py'), "/home/user/etl_pipeline.py is missing."
    assert os.path.isfile('/home/user/run_etl.sh'), "/home/user/run_etl.sh is missing."

    st = os.stat('/home/user/run_etl.sh')
    assert bool(st.st_mode & stat.S_IXUSR), "/home/user/run_etl.sh is not executable."

def test_cron_job_scheduled():
    """Verify that the cron job is scheduled to run every 5 minutes."""
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Is cron configured for the user?"
    crontab_content = result.stdout

    found = False
    for line in crontab_content.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                command = " ".join(parts[5:])
                if schedule == "*/5 * * * *" and "/home/user/run_etl.sh" in command:
                    found = True
                    break
    assert found, "Cron job for run_etl.sh running every 5 minutes (*/5 * * * *) is not scheduled correctly."

def test_etl_execution_and_idempotency():
    """Run the ETL script twice to ensure it works and handles idempotency properly."""
    # First execution
    res1 = subprocess.run(['/home/user/run_etl.sh'], capture_output=True, text=True)
    assert res1.returncode == 0, f"First execution of run_etl.sh failed:\nSTDOUT: {res1.stdout}\nSTDERR: {res1.stderr}"

    # Second execution (retry simulation)
    res2 = subprocess.run(['/home/user/run_etl.sh'], capture_output=True, text=True)
    assert res2.returncode == 0, f"Second execution of run_etl.sh failed:\nSTDOUT: {res2.stdout}\nSTDERR: {res2.stderr}"

    parquet_file = '/home/user/data/processed/master.parquet'
    assert os.path.isfile(parquet_file), f"{parquet_file} was not created."

    # Use a python subprocess to read the parquet file and output JSON
    # This avoids importing pandas directly in the pytest environment
    check_script = f"""
import pandas as pd
import json
import sys

try:
    df = pd.read_parquet('{parquet_file}')
    records = df.to_dict(orient='records')
    print(json.dumps(records))
except Exception as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)
"""
    res_py = subprocess.run(['python3', '-c', check_script], capture_output=True, text=True)
    assert res_py.returncode == 0, f"Failed to read parquet file using pandas:\n{res_py.stderr}"

    try:
        data = json.loads(res_py.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Could not parse output from parquet reader. Output was: {res_py.stdout}")

    # Verify row count
    assert len(data) == 5, f"Expected exactly 5 records in master.parquet after retries (idempotency failed), but found {len(data)}."

    # Verify specific record calculations
    r005 = next((row for row in data if row.get('request_id') == 'r005'), None)
    assert r005 is not None, "Record 'r005' not found in master.parquet."
    assert r005.get('user_id') == 'u1', f"Expected user_id 'u1' for r005, got {r005.get('user_id')}."

    try:
        resp_time = float(r005.get('response_time', 0))
        rolling_avg = float(r005.get('rolling_avg_time', 0))
    except (TypeError, ValueError):
        pytest.fail(f"Invalid types for metrics in r005: {r005}")

    assert resp_time == 100.0, f"Expected response_time 100.0 for r005, got {resp_time}."
    assert rolling_avg == 150.0, f"Expected rolling_avg_time 150.0 for r005, got {rolling_avg}."