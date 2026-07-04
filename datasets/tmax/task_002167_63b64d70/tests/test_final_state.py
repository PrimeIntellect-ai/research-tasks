# test_final_state.py

import os
import stat

def test_deploy_supervisor_exists_and_executable():
    """Test that /home/user/deploy_supervisor.py exists and is executable."""
    script_file = "/home/user/deploy_supervisor.py"
    assert os.path.exists(script_file), f"File {script_file} does not exist."
    assert os.path.isfile(script_file), f"{script_file} is not a regular file."

    st = os.stat(script_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_file} is not executable."

def test_app_conf_updated():
    """Test that /home/user/app.conf has insecure_mode=false."""
    conf_file = "/home/user/app.conf"
    assert os.path.exists(conf_file), f"File {conf_file} does not exist."

    with open(conf_file, 'r') as f:
        content = f.read()

    assert "insecure_mode=false" in content, f"{conf_file} does not contain 'insecure_mode=false'."
    assert "insecure_mode=true" not in content, f"{conf_file} still contains 'insecure_mode=true'."

def test_deploy_log_content():
    """Test that /home/user/deploy.log contains the success message."""
    log_file = "/home/user/deploy.log"
    assert os.path.exists(log_file), f"File {log_file} does not exist. The supervisor script may not have run successfully."

    with open(log_file, 'r') as f:
        lines = f.readlines()

    content = "".join(lines)
    assert "Deployment Secure" in content, f"Expected 'Deployment Secure' in {log_file}, but got: {content}"

def test_deploy_count():
    """Test that the legacy script was retried the correct number of times."""
    count_file = "/home/user/.deploy_count"
    assert os.path.exists(count_file), f"File {count_file} does not exist. The legacy script was likely not executed."

    with open(count_file, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Expected a number in {count_file}, got: {content}"
    count = int(content)
    assert count >= 3, f"Expected deploy count to be at least 3, got: {count}"