# test_final_state.py
import os

def get_mount_point():
    fstab_path = "/home/user/mock_fstab"
    if not os.path.exists(fstab_path):
        return "/home/user/metrics_mount"
    with open(fstab_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0] == "/dev/sda1":
                return parts[1]
    return "/home/user/metrics_mount"

def test_expect_script_exists():
    path = "/home/user/auto_fetch.exp"
    assert os.path.isfile(path), f"Expect script missing at {path}"

def test_go_program_exists():
    path = "/home/user/analyzer.go"
    assert os.path.isfile(path), f"Go program missing at {path}"

def test_raw_logs_content():
    mount_point = get_mount_point()
    raw_logs_path = os.path.join(mount_point, "raw_logs.txt")
    assert os.path.isfile(raw_logs_path), f"raw_logs.txt missing at {raw_logs_path}"

    with open(raw_logs_path, "r") as f:
        content = f.read()

    assert "2024-01-10T02:15:00Z | Database failover" in content, "Missing first raw log line"
    assert "2024-01-15T14:45:00Z | API gateway timeout" in content, "Missing second raw log line"
    assert "2024-02-01T23:59:00Z | Scheduled maintenance" in content, "Missing third raw log line"

def test_processed_logs_content():
    mount_point = get_mount_point()
    processed_logs_path = os.path.join(mount_point, "processed_logs.txt")
    assert os.path.isfile(processed_logs_path), f"processed_logs.txt missing at {processed_logs_path}"

    expected_lines = [
        "2024-01-10 11:15:00 JST - Database failover",
        "2024-01-15 23:45:00 JST - API gateway timeout",
        "2024-02-02 08:59:00 JST - Scheduled maintenance"
    ]

    with open(processed_logs_path, "r") as f:
        content = f.read()

    for line in expected_lines:
        assert line in content, f"Expected processed log line missing: {line}"