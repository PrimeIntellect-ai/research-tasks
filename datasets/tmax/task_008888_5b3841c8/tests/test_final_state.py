# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    cargo_toml = "/home/user/quota_monitor/Cargo.toml"
    main_rs = "/home/user/quota_monitor/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Rust project file {cargo_toml} is missing. Did you create the project?"
    assert os.path.isfile(main_rs), f"Rust source file {main_rs} is missing."

def test_quota_alerts_log():
    fstab_path = "/home/user/custom_fstab"
    passwd_path = "/home/user/mock_passwd"
    log_path = "/home/user/quota_alerts.log"

    assert os.path.isfile(fstab_path), f"File {fstab_path} is missing."
    assert os.path.isfile(passwd_path), f"File {passwd_path} is missing."
    assert os.path.isfile(log_path), f"Output log file {log_path} was not generated."

    # Parse mock_passwd
    uid_to_user = {}
    with open(passwd_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(':')
            if len(parts) >= 3:
                username = parts[0]
                uid = parts[2]
                uid_to_user[uid] = username

    # Parse custom_fstab and compute expected alerts
    expected_alerts = []
    with open(fstab_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 4:
                mount_point = parts[1]
                options = parts[3].split(',')

                uid = None
                quota = None
                for opt in options:
                    if opt.startswith('uid='):
                        uid = opt.split('=')[1]
                    elif opt.startswith('quota='):
                        quota = int(opt.split('=')[1])

                if uid and quota is not None:
                    username = uid_to_user.get(uid)
                    if not username:
                        continue

                    data_file = os.path.join(mount_point, "data.bin")
                    if os.path.isfile(data_file):
                        usage = os.path.getsize(data_file)
                        if usage > quota:
                            alert = f"ALERT: User {username} exceeded quota on {mount_point}. Usage: {usage} bytes, Limit: {quota} bytes."
                            expected_alerts.append((username, alert))

    # Sort alphabetically by username as per instructions
    expected_alerts.sort(key=lambda x: x[0])
    expected_lines = [alert for _, alert in expected_alerts]

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {log_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )