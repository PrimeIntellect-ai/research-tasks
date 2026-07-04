# test_final_state.py

import os
import stat
import json
import pytest

def test_rust_binary_compiled():
    binary_path = "/home/user/migrator/target/release/migrator"
    assert os.path.isfile(binary_path), f"Rust release binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

def test_apply_routes_script():
    script_path = "/home/user/output/apply_routes.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist"

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {script_path} is not executable"

    with open(script_path, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 1, f"{script_path} is empty"
    assert content[0] == "#!/bin/bash", f"{script_path} does not start with #!/bin/bash"

    # Check for correct routes
    expected_routes = [
        "ip route add 10.5.1.100/32 via 10.99.0.1",
        "ip route add 10.5.1.102/32 via 10.99.0.1"
    ]

    # Filter out empty lines or just shebang
    actual_routes = [line.strip() for line in content[1:] if line.strip()]

    assert actual_routes == expected_routes, f"Routes in {script_path} do not match expected output. Got: {actual_routes}"

def test_mock_fstab():
    fstab_path = "/home/user/output/mock_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist"

    with open(fstab_path, "r") as f:
        content = [line.strip() for line in f.readlines() if line.strip()]

    expected_fstab = [
        "10.10.10.50:/vol/db-main /home/user/mnt/db-main nfs defaults,user,noauto 0 0",
        "10.10.10.51:/vol/assets /home/user/mnt/assets nfs defaults,user,noauto 0 0"
    ]

    assert content == expected_fstab, f"Fstab entries in {fstab_path} do not match expected output. Got: {content}"

def test_crontab_dump():
    dump_path = "/home/user/output/crontab_dump.txt"
    assert os.path.isfile(dump_path), f"File {dump_path} does not exist"

    with open(dump_path, "r") as f:
        content = f.read()

    expected_cron = "*/5 * * * * /home/user/migrator/target/release/migrator"
    assert expected_cron in content, f"Expected cron job '{expected_cron}' not found in {dump_path}"