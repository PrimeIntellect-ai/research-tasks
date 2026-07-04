# test_final_state.py
import os
import subprocess
import pytest

def test_monitor_binary_exists_and_size():
    """Check that /app/monitor exists, is executable, and its size is <= 3,000,000 bytes."""
    monitor_path = "/app/monitor"
    assert os.path.exists(monitor_path), f"Compiled binary {monitor_path} does not exist."
    assert os.path.isfile(monitor_path), f"{monitor_path} is not a file."
    assert os.access(monitor_path, os.X_OK), f"{monitor_path} is not executable."

    size = os.path.getsize(monitor_path)
    threshold = 3000000
    assert size <= threshold, f"Binary size of {monitor_path} is {size} bytes, which exceeds the maximum allowed {threshold} bytes. Did you strip debug symbols?"

def test_monitor_execution_and_output():
    """Execute /app/monitor and check the output in /app/status.txt."""
    monitor_path = "/app/monitor"
    status_path = "/app/status.txt"

    # Ensure services are running before executing monitor
    subprocess.run(["/app/start_services.sh"], check=False)

    # Remove status.txt if it exists to ensure fresh output
    if os.path.exists(status_path):
        os.remove(status_path)

    # Execute the monitor
    result = subprocess.run([monitor_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {monitor_path} failed with return code {result.returncode}. stderr: {result.stderr}"

    assert os.path.exists(status_path), f"Output file {status_path} was not created by the monitor."

    with open(status_path, "r") as f:
        content = f.read().strip()

    expected_content = "nginx: 200, api: 200"
    assert content == expected_content, f"Content of {status_path} is '{content}', expected '{expected_content}'."

def test_crontab_configuration():
    """Check that the crontab is configured to run /app/monitor every minute."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    crontab_content = result.stdout.strip()

    # Check for the presence of the cron job
    # It should be '* * * * * /app/monitor' or similar
    found = False
    for line in crontab_content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            command = " ".join(parts[5:])
            if schedule == "* * * * *" and "/app/monitor" in command:
                found = True
                break

    assert found, "Crontab does not contain a job scheduling /app/monitor every minute (* * * * *)."