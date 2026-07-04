# test_final_state.py
import os
import time
import socket
import requests
import subprocess
import json

def test_log_processor_tcp_and_http():
    # Get initial stats if possible
    try:
        r = requests.get("http://127.0.0.1:9001/stats", timeout=2)
        initial_data = r.json()
        initial_unique = initial_data.get("unique", 0)
        initial_duplicates = initial_data.get("duplicates", 0)
    except Exception:
        initial_unique = 0
        initial_duplicates = 0

    # Inject custom records
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 9000))
        s.sendall(b"1690000000,req_test_100,10.0.0.1,test@domain.com,login,1\n")
        s.sendall(b"1690000001,req_test_100,10.0.0.1,test@domain.com,login,1\n") # Duplicate
        s.sendall(b"1690000002,req_test_101,10.0.0.2,admin@domain.com,logout,0\n")
    except Exception as e:
        assert False, f"Failed to connect and send data to TCP 9000: {e}"
    finally:
        s.close()

    time.sleep(1)

    # Check metrics via HTTP
    try:
        r = requests.get("http://127.0.0.1:9001/stats", timeout=2)
    except Exception as e:
        assert False, f"Failed to connect to HTTP 9001: {e}"

    assert r.status_code == 200, f"Expected HTTP 200, got {r.status_code}"
    assert "application/json" in r.headers.get("Content-Type", ""), "Expected Content-Type: application/json"

    try:
        data = r.json()
    except Exception:
        assert False, f"Failed to parse JSON response: {r.text}"

    assert "unique" in data and "duplicates" in data, "JSON response missing required keys"

    # We injected 2 unique and 1 duplicate. The counts should have increased by at least these amounts.
    assert data["unique"] >= initial_unique + 2, f"Expected at least {initial_unique + 2} unique records, got {data['unique']}"
    assert data["duplicates"] >= initial_duplicates + 1, f"Expected at least {initial_duplicates + 1} duplicate records, got {data['duplicates']}"

def test_data_masking():
    log_file = "/home/user/processed_logs.csv"
    assert os.path.exists(log_file), f"Log file {log_file} does not exist"

    with open(log_file, "r") as f:
        content = f.read()

    # Check if the injected records are masked correctly
    assert "10.0.0.XXX" in content, "IP address not masked correctly (expected 10.0.0.XXX)"
    assert "***@domain.com" in content, "Email not masked correctly (expected ***@domain.com)"
    assert "10.0.0.1" not in content, "Unmasked IP address found in logs"
    assert "test@domain.com" not in content, "Unmasked email found in logs"

def test_rotation_script():
    script_file = "/home/user/rotate.sh"
    log_file = "/home/user/processed_logs.csv"
    archive_dir = "/home/user/archive"

    assert os.path.exists(script_file), f"Rotation script {script_file} does not exist"
    assert os.path.isdir(archive_dir), f"Archive directory {archive_dir} does not exist"

    # Write some dummy data to ensure it's not empty
    with open(log_file, "a") as f:
        f.write("dummy_data\n")

    initial_size = os.path.getsize(log_file)
    assert initial_size > 0, "Log file is empty before rotation"

    # Count archive files before
    archives_before = set(os.listdir(archive_dir))

    # Run rotation script
    try:
        subprocess.run(["bash", script_file], check=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Rotation script failed: {e}"

    # Check if original file is truncated
    final_size = os.path.getsize(log_file)
    assert final_size == 0, "Log file was not truncated after rotation"

    # Check if a new archive file was created
    archives_after = set(os.listdir(archive_dir))
    new_archives = archives_after - archives_before
    assert len(new_archives) >= 1, "No new archive file was created in the archive directory"

def test_cron_configuration():
    try:
        crontab = subprocess.check_output(["crontab", "-l"]).decode()
    except subprocess.CalledProcessError:
        assert False, "Failed to read crontab for user"

    assert "/home/user/rotate.sh" in crontab, "Rotation script not found in crontab"

    # Check for the schedule * * * * *
    lines = crontab.splitlines()
    found_schedule = False
    for line in lines:
        if line.strip().startswith("#"):
            continue
        if "/home/user/rotate.sh" in line and "* * * * *" in line:
            found_schedule = True
            break

    assert found_schedule, "Crontab does not have the exact '* * * * *' schedule for rotate.sh"