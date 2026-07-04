# test_final_state.py
import os
import pytest

def get_large_directories(base_dir, threshold_bytes=10 * 1024 * 1024):
    large_dirs = []
    if not os.path.isdir(base_dir):
        return large_dirs

    for d in os.listdir(base_dir):
        dir_path = os.path.join(base_dir, d)
        if os.path.isdir(dir_path):
            total_size = 0
            for dirpath, _, filenames in os.walk(dir_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            if total_size > threshold_bytes:
                large_dirs.append(d)
    return large_dirs

def test_finops_fstab_generated():
    fstab_path = "/home/user/finops_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    large_dirs = get_large_directories("/home/user/s3_cache")
    assert len(large_dirs) > 0, "No large directories found to test against."

    expected_lines = []
    for d in large_dirs:
        expected_lines.append(f"/home/user/s3_cache/{d} /home/user/cold_tier/{d} none bind 0 0")

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {fstab_path}."

    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} lines in {fstab_path}, found {len(lines)}."

def test_finops_env_generated():
    env_path = "/home/user/finops_env.sh"
    assert os.path.isfile(env_path), f"File {env_path} does not exist."

    with open(env_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    large_dirs = get_large_directories("/home/user/s3_cache")

    expected_lines = []
    for d in large_dirs:
        expected_lines.append(f"export {d.upper()}_STORAGE_TIER=cold")

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {env_path}."

    assert len(lines) == len(expected_lines), f"Expected exactly {len(expected_lines)} lines in {env_path}, found {len(lines)}."

def test_systemd_service():
    service_path = "/home/user/.config/systemd/user/finops-tiering.service"
    assert os.path.isfile(service_path), f"Systemd service file {service_path} does not exist."

    with open(service_path, 'r') as f:
        content = f.read()

    assert "Type=oneshot" in content, f"'Type=oneshot' not found in {service_path}."
    assert "ExecStart=/usr/bin/python3 /home/user/finops_tiering.py" in content, f"Expected ExecStart not found in {service_path}."