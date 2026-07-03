# test_final_state.py

import os
import re
import subprocess
import pytest

def test_drift_report_mse():
    report_path = '/home/user/drift_report.txt'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        content = f.read()

    matches = re.findall(r'Rolling average config size: (\d+\.\d{2}) bytes', content)
    assert len(matches) == 5, f"Expected exactly 5 rolling average entries, found {len(matches)}."

    expected = [1055.50, 1072.00, 1110.00, 1118.00, 1131.67]
    actual = [float(m) for m in matches]

    mse = sum((a - e)**2 for a, e in zip(actual, expected)) / len(expected)
    assert mse <= 0.01, f"MSE {mse} is greater than threshold 0.01. Actual values: {actual}"

def test_cron_job_setup():
    try:
        result = subprocess.run(
            ['crontab', '-l', '-u', 'user'],
            capture_output=True,
            text=True,
            check=True
        )
        cron_output = result.stdout
    except subprocess.CalledProcessError:
        # Fallback to checking the crontab file directly if crontab command fails
        crontab_file = '/var/spool/cron/crontabs/user'
        if os.path.exists(crontab_file):
            with open(crontab_file, 'r') as f:
                cron_output = f.read()
        else:
            pytest.fail("Failed to retrieve crontab for 'user'.")

    assert '/home/user/drift_monitor/target/release/drift_monitor' in cron_output, \
        "Cron job for drift_monitor release binary is not set up correctly."
    assert '* * * * *' in cron_output, "Cron job is not scheduled to run every minute."