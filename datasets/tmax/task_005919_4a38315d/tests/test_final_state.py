# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_migration_env_file():
    path = "/home/user/migration_env.sh"
    assert os.path.isfile(path), f"File {path} must exist."
    with open(path, "r") as f:
        content = f.read()
    assert "TZ" in content and "Asia/Tokyo" in content, "TZ must be exported as Asia/Tokyo"
    assert "LC_ALL" in content and "C" in content, "LC_ALL must be exported as C"
    assert "MAX_DISK_KB" in content and "10240" in content, "MAX_DISK_KB must be exported as 10240"

def test_migration_data_payload():
    path = "/home/user/migration_data/payload.bin"
    assert os.path.isfile(path), f"File {path} must exist."
    size = os.path.getsize(path)
    assert size == 12582912, f"File {path} must be exactly 12288 KB (12582912 bytes), but got {size} bytes."

def test_apptainer_instance_running():
    result = subprocess.run(["apptainer", "instance", "list"], capture_output=True, text=True)
    assert "service_migrator" in result.stdout, "Apptainer instance 'service_migrator' must be running."

def test_check_readiness_script():
    path = "/home/user/check_readiness.sh"
    assert os.path.isfile(path), f"File {path} must exist."
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"File {path} must be executable."

def test_final_status_log():
    path = "/home/user/final_status.log"
    assert os.path.isfile(path), f"File {path} must exist."
    with open(path, "r") as f:
        content = f.read().strip()

    # Expected output regex: ^\[2024-03-10 01:00:00\] INSTANCE:RUNNING DISK_KB:122(88|92) LIMIT:EXCEEDED$
    pattern = r"^\[2024-03-10 01:00:00\] INSTANCE:RUNNING DISK_KB:\d+ LIMIT:EXCEEDED$"
    assert re.match(pattern, content), f"File {path} content '{content}' does not match expected format."

    # Extract DISK_KB to ensure it's > 10240
    match = re.search(r"DISK_KB:(\d+)", content)
    assert match, "DISK_KB value not found in log."
    disk_kb = int(match.group(1))
    assert disk_kb > 10240, f"DISK_KB {disk_kb} should be greater than 10240."