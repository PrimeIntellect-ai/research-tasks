# test_final_state.py

import os
import re
import subprocess
import pytest

def test_migrator_cpp_exists():
    """Verify that the C++ source file exists."""
    path = "/home/user/migrator.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_migrator_binary_exists_and_executable():
    """Verify that the compiled binary exists and is executable."""
    path = "/home/user/migrator"
    assert os.path.isfile(path), f"Binary {path} does not exist."
    assert os.access(path, os.X_OK), f"Binary {path} is not executable."

def test_automate_exp_exists_and_executable():
    """Verify that the Expect script exists, is executable, and has the correct shebang."""
    path = "/home/user/automate.exp"
    assert os.path.isfile(path), f"Expect script {path} does not exist."
    assert os.access(path, os.X_OK), f"Expect script {path} is not executable."

    with open(path, 'r') as f:
        first_line = f.readline().strip()
    assert first_line == "#!/usr/bin/expect", f"Expect script {path} does not start with #!/usr/bin/expect."

def test_fstab_entry_correct():
    """Verify that the fstab entry file exists and contains the correct configuration."""
    path = "/home/user/fstab_entry.txt"
    assert os.path.isfile(path), f"fstab entry file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    # Regex to match: /dev/xvdf /tmp/migration_data ext4 defaults,noatime 0 2
    # with any whitespace between fields
    pattern = r"^/dev/xvdf\s+/tmp/migration_data\s+ext4\s+defaults,noatime\s+0\s+2$"
    assert re.match(pattern, content), f"Content of {path} does not match the required fstab entry format. Found: {content}"

def test_automate_exp_execution_and_status_file():
    """Verify that running the Expect script successfully creates the status file with correct content."""
    script_path = "/home/user/automate.exp"
    status_path = "/home/user/migration_status.txt"

    # Remove the status file if it already exists to ensure the script creates it
    if os.path.exists(status_path):
        os.remove(status_path)

    # Execute the expect script
    result = subprocess.run([script_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"Expect script failed to execute. STDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    # Check that the status file was created
    assert os.path.isfile(status_path), f"Status file {status_path} was not created after running the expect script."

    # Verify the content of the status file
    with open(status_path, 'r') as f:
        content = f.read().strip()
    assert content == "MIGRATION_READY", f"Status file {status_path} contains incorrect text: {content}"