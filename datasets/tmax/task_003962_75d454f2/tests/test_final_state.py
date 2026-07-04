# test_final_state.py

import os
import subprocess
import re

def test_merged_timeline_log():
    path = "/home/user/merged_timeline.log"
    assert os.path.isfile(path), f"{path} is missing. You must create the merged log file."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected_lines = [
        "2023-10-01 10:00:01 [WEB] Service ping OK",
        "2023-10-01 10:00:02 [API] Endpoint active",
        "2023-10-01 10:00:05 [DB] Query successful",
        "2023-10-01 10:00:10 [API] Endpoint active",
        "2023-10-01 10:00:15 [WEB] Service ping OK",
        "2023-10-01 10:00:20 [DB] Query successful",
        "2023-10-01 10:00:35 [DB] Query slow",
        "2023-10-01 10:00:45 [WEB] Timeout reached",
        "2023-10-01 10:00:50 [API] Error 503"
    ]

    assert lines == expected_lines, f"Contents of {path} do not match the expected chronologically sorted logs. Make sure to merge all three logs and sort them properly."

def test_mre_script():
    path = "/home/user/mre.sh"
    assert os.path.isfile(path), f"{path} is missing. You must create the MRE script."
    assert os.access(path, os.X_OK), f"{path} is not executable. Run chmod +x on it."

    # Run the script
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} failed with exit code {result.returncode}. It should exit 0 if a leak is successfully demonstrated. Error output: {result.stderr}"

    output = result.stdout.strip()
    assert output, f"{path} produced no output. It must output the number of orphaned sleep processes."

    # Try to find a positive integer in the output
    numbers = re.findall(r'\b[1-9][0-9]*\b', output)
    assert numbers, f"{path} did not output a number > 0 indicating orphaned processes. Output was: '{output}'"

def test_uptime_fixed_script():
    path = "/home/user/monitor/uptime_fixed.sh"
    assert os.path.isfile(path), f"{path} is missing. You must create the fixed monitoring script."
    assert os.access(path, os.X_OK), f"{path} is not executable. Run chmod +x on it."

def test_regression_script():
    path = "/home/user/regression.sh"
    assert os.path.isfile(path), f"{path} is missing. You must create the regression test script."
    assert os.access(path, os.X_OK), f"{path} is not executable. Run chmod +x on it."

    # Run the script
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} failed with exit code {result.returncode}. It should exit 0 if the test passes (no leak). Output: {result.stderr}\n{result.stdout}"

    # Ensure no sleep processes from the test are left behind
    ps_result = subprocess.run(["pgrep", "-f", "sleep"], capture_output=True, text=True)
    # Note: there might be other sleep processes in the system, but typically in this isolated container there shouldn't be long running sleeps.
    # We mainly rely on the script's own verification and exit code as per instructions.