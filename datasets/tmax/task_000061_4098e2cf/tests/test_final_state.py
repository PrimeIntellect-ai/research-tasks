# test_final_state.py
import os
import time
import subprocess

def test_monitor_profile_exists_and_configured():
    profile_path = "/home/user/.monitor_profile"
    assert os.path.exists(profile_path), f"{profile_path} is missing."
    with open(profile_path, "r") as f:
        content = f.read()
    assert "ALERT_THRESHOLD=90" in content, "ALERT_THRESHOLD=90 not found in .monitor_profile"
    assert "ALERT_EMAIL=admin@local.dev" in content, "ALERT_EMAIL=admin@local.dev not found in .monitor_profile"

def test_scripts_are_executable():
    assert os.access("/home/user/monitor.py", os.X_OK), "monitor.py is not executable"
    assert os.access("/home/user/supervisor.sh", os.X_OK), "supervisor.sh is not executable"

def test_supervisor_running():
    output = subprocess.check_output(["ps", "aux"]).decode()
    assert "supervisor.sh" in output, "supervisor.sh is not running in the background"

def test_alert_pipeline_and_supervisor_restart():
    cpu_file = "/home/user/cpu.txt"
    email_log = "/home/user/email_out.log"

    # Step 1: Write a value > 90 to cpu.txt
    with open(cpu_file, "w") as f:
        f.write("95\n")
    time.sleep(2)

    # Step 2: Read email_out.log and assert first email
    assert os.path.exists(email_log), f"{email_log} was not created by the mock SMTP server."
    with open(email_log, "r") as f:
        log_content = f.read()

    assert "Subject: CPU Alert" in log_content, "Expected 'Subject: CPU Alert' in email log"
    assert "admin@local.dev" in log_content, "Expected destination 'admin@local.dev' in email log"

    initial_email_count = log_content.count("Subject: CPU Alert")
    assert initial_email_count >= 1, "No email found in log after exceeding threshold."

    # Step 3: Kill the monitor.py process to test the supervisor
    subprocess.run(["pkill", "-f", "monitor.py"])
    time.sleep(3)

    # Step 4: Reset the threshold to prime the alert
    with open(cpu_file, "w") as f:
        f.write("50\n")
    time.sleep(2)

    # Step 5: Trigger a second alert
    with open(cpu_file, "w") as f:
        f.write("99\n")
    time.sleep(3)  # wait for monitor to pick it up

    # Step 6: Read email_out.log and assert second email is logged
    with open(email_log, "r") as f:
        log_content_after = f.read()

    final_email_count = log_content_after.count("Subject: CPU Alert")
    assert final_email_count > initial_email_count, (
        "Supervisor did not restart monitor.py successfully, or the second alert was not sent."
    )