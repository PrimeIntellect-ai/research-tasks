# test_final_state.py

import os
import subprocess
import time
import tarfile
import urllib.request
import urllib.error

def test_setup_done():
    """Check if the setup_done.txt file exists and contains 'READY'."""
    setup_file = '/home/user/setup_done.txt'
    assert os.path.isfile(setup_file), f"Setup file {setup_file} does not exist."
    with open(setup_file, 'r') as f:
        content = f.read().strip()
    assert content == "READY", f"Expected 'READY' in {setup_file}, found '{content}'."

def test_cron_job_exists():
    """Verify that the cron job for restore_tester.py is installed for 'user'."""
    try:
        result = subprocess.run(['su', '-', 'user', '-c', 'crontab -l'], capture_output=True, text=True, check=True)
        assert 'restore_tester.py' in result.stdout, "Cron job for restore_tester.py not found in crontab."
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to read crontab for user 'user': {e.stderr}"

def test_nginx_running():
    """Verify that Nginx is running with the user's config."""
    try:
        result = subprocess.run(['pgrep', '-f', 'nginx.*nginx.conf'], capture_output=True, text=True)
        assert result.returncode == 0, "Nginx is not running with the custom nginx.conf."
    except Exception as e:
        assert False, f"Error checking Nginx process: {e}"

def test_end_to_end_restore_tester():
    """
    Test the restore_tester.py script end-to-end:
    - Create a test tarball
    - Run the script manually
    - Fetch the file via Nginx
    - Verify file permissions
    - Verify tarball moved to processed directory
    """
    inbox_dir = '/home/user/restore_inbox'
    active_dir = '/home/user/restore_active'
    processed_dir = '/home/user/restore_processed'

    # Ensure directories exist (script should have created them, or user setup)
    assert os.path.isdir(inbox_dir), f"{inbox_dir} does not exist."
    assert os.path.isdir(active_dir), f"{active_dir} does not exist."
    assert os.path.isdir(processed_dir), f"{processed_dir} does not exist."

    # Create test tarball
    test_tar_name = 'backup_test99.tar.gz'
    test_tar_path = os.path.join(inbox_dir, test_tar_name)
    test_dir_name = 'backup_test99'
    test_file_name = 'test_data.txt'
    test_content = "INTEGRATION_SUCCESS"

    tmp_dir = '/tmp/backup_test_dir'
    os.makedirs(tmp_dir, exist_ok=True)
    tmp_file_path = os.path.join(tmp_dir, test_file_name)

    with open(tmp_file_path, 'w') as f:
        f.write(test_content)

    with tarfile.open(test_tar_path, "w:gz") as tar:
        tar.add(tmp_file_path, arcname=test_file_name)

    # Change ownership to user
    subprocess.run(['chown', 'user:user', test_tar_path], check=True)

    # Run the script manually
    try:
        subprocess.run(['su', '-', 'user', '-c', 'python3 /home/user/restore_tester.py'], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"restore_tester.py failed to execute: {e.stderr}"

    # Wait a moment for Nginx to reload and background server to start
    time.sleep(2)

    # Test via Nginx
    url = f"http://127.0.0.1:8080/{test_dir_name}/{test_file_name}"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        response = req.read().decode('utf-8').strip()
        assert test_content in response, f"Expected '{test_content}' in response, got '{response}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to retrieve data via proxy at {url}: {e}"

    # Verify permissions
    extracted_file_path = os.path.join(active_dir, test_dir_name, test_file_name)
    assert os.path.isfile(extracted_file_path), f"Extracted file not found at {extracted_file_path}"

    mode = os.stat(extracted_file_path).st_mode
    perms = oct(mode)[-3:]
    assert perms == '640', f"Incorrect file permissions for {extracted_file_path}: expected 640, got {perms}"

    # Verify processed
    processed_tar_path = os.path.join(processed_dir, test_tar_name)
    assert os.path.isfile(processed_tar_path), f"Tarball was not moved to {processed_tar_path}"