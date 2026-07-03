# test_final_state.py
import os
import shutil
import tarfile
import subprocess
import urllib.request
import urllib.error
from datetime import datetime
import pytest

try:
    import zoneinfo
except ImportError:
    zoneinfo = None

def test_web_service_success():
    """Verify that the Nginx + Python app setup is fixed and returns 200 OK."""
    url = "http://127.0.0.1:8080"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        status_code = req.getcode()
        content = req.read().decode('utf-8').strip()

        assert status_code == 200, f"Expected status code 200, got {status_code}"
        assert content == "Success", f"Expected response body 'Success', got '{content}'"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Service returned an HTTP error: {e.code} {e.reason}. The Nginx/Python socket configuration is likely still incorrect.")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url}: {e.reason}. Ensure both Nginx and the Python app are running.")
    except Exception as e:
        pytest.fail(f"Unexpected error when testing the web service: {e}")

def test_acl_permissions():
    """Verify that the user 'nobody' has r-x ACL permissions on /home/user/service/public."""
    target_dir = "/home/user/service/public"
    assert os.path.exists(target_dir), f"Directory {target_dir} does not exist."

    try:
        out = subprocess.check_output(["getfacl", target_dir], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to execute getfacl on {target_dir}: {e.output}")

    assert "user:nobody:r-x" in out, "ACL for user 'nobody' is not set to 'r-x' (read and execute) on the target directory."

def test_backup_archive():
    """Verify the legacy data backup archive exists and contains the correct files."""
    archive_path = "/home/user/legacy_data_backup.tar.gz"
    assert os.path.exists(archive_path), f"Backup archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        assert any("file1.txt" in name for name in names), "file1.txt is missing from the backup archive."
        assert any("file2.txt" in name for name in names), "file2.txt is missing from the backup archive."

def test_storage_status():
    """Verify the storage monitoring script correctly evaluated the free space."""
    status_file = "/home/user/storage_status.txt"
    assert os.path.exists(status_file), f"Storage status file {status_file} was not created."

    free_space = shutil.disk_usage("/").free
    expected_status = "OK" if free_space > 1048576 else "FULL"

    with open(status_file, "r") as f:
        actual_status = f.read().strip()

    assert actual_status == expected_status, f"Expected storage status '{expected_status}' based on current free space, but got '{actual_status}'."

def test_timezone_conversion():
    """Verify the timezone conversion script correctly converted UTC to America/New_York."""
    input_file = "/home/user/events.log"
    output_file = "/home/user/events_ny.log"

    assert os.path.exists(output_file), f"Converted log file {output_file} does not exist."

    expected_lines = []
    if os.path.exists(input_file) and zoneinfo is not None:
        # Dynamically compute expected output if input exists and zoneinfo is available
        with open(input_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                dt = datetime.strptime(line, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
                dt_ny = dt.astimezone(zoneinfo.ZoneInfo("America/New_York"))
                expected_lines.append(dt_ny.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        # Fallback to the known truth values if dynamic computation isn't possible
        expected_lines = [
            "2023-10-01 08:00:00",
            "2023-12-25 12:30:00",
            "2024-03-10 02:15:00"
        ]

    with open(output_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Converted timestamps in {output_file} do not match the expected America/New_York values."