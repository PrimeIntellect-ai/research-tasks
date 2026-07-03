# test_final_state.py
import os
import subprocess

def test_provision_script_exists():
    assert os.path.isfile("/home/user/provision.py"), "/home/user/provision.py does not exist."

def test_provision_script_behavior():
    script_path = "/home/user/provision.py"
    test_user = "pytest_tenant_user"

    # Run the script
    process = subprocess.Popen(
        ["python3", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=f"{test_user}\n")

    # Check exit code
    assert process.returncode == 0, f"Script exited with code {process.returncode}. Stderr: {stderr}"

    # Check stdout
    assert "Enter username:" in stdout, "Script did not prompt with 'Enter username:'"
    assert "Success" in stdout, "Script did not print 'Success'"

    # Check created directories
    data_dir = f"/home/user/tenants/{test_user}/data"
    logs_dir = f"/home/user/tenants/{test_user}/logs"
    assert os.path.isdir(data_dir), f"Directory {data_dir} was not created."
    assert os.path.isdir(logs_dir), f"Directory {logs_dir} was not created."

    # Check .quota file
    quota_file = f"/home/user/tenants/{test_user}/.quota"
    assert os.path.isfile(quota_file), f"File {quota_file} was not created."
    with open(quota_file, "r") as f:
        content = f.read().strip()
    assert content == "10GB", f"Expected '10GB' in {quota_file}, found '{content}'"

    # Check log file
    log_file = "/home/user/provision_log.txt"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."
    with open(log_file, "r") as f:
        log_content = f.read()
    expected_log = f"Provisioned {test_user}\n"
    assert expected_log in log_content, f"Expected '{expected_log.strip()}' to be in {log_file}"