# test_final_state.py
import os
import subprocess

def test_fstab_conf():
    path = "/home/user/fstab.conf"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "/home/user/data_source /home/user/data_dest",
        "/home/user/log_source /home/user/log_dest"
    ]
    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {path}."

def test_symlinks_and_directories():
    dirs = [
        "/home/user/data_source",
        "/home/user/data_dest",
        "/home/user/log_source",
        "/home/user/log_dest"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

    links = {
        "/home/user/data_dest/mnt": "/home/user/data_source",
        "/home/user/log_dest/mnt": "/home/user/log_source"
    }
    for link_path, target in links.items():
        assert os.path.islink(link_path), f"{link_path} is not a symlink."
        actual_target = os.readlink(link_path)
        assert actual_target == target, f"Symlink {link_path} points to {actual_target}, expected {target}."

def test_setup_mounts_idempotency():
    script_path = "/home/user/setup_mounts.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the script again to verify idempotency
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed on second run. Not idempotent. Stderr: {result.stderr}"

    # Check symlinks are still correct and not nested
    links = {
        "/home/user/data_dest/mnt": "/home/user/data_source",
        "/home/user/log_dest/mnt": "/home/user/log_source"
    }
    for link_path, target in links.items():
        assert os.path.islink(link_path), f"{link_path} is no longer a symlink after second run."
        actual_target = os.readlink(link_path)
        assert actual_target == target, f"Symlink {link_path} points to {actual_target} after second run, expected {target}."

def test_supervisor_compiled():
    c_file = "/home/user/supervisor.c"
    bin_file = "/home/user/supervisor"

    assert os.path.isfile(c_file), f"{c_file} is missing."
    assert os.path.isfile(bin_file), f"{bin_file} is missing."
    assert os.access(bin_file, os.X_OK), f"{bin_file} is not executable."

def test_failing_service_script():
    script_path = "/home/user/failing_service.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_migration_result():
    log_path = "/home/user/migration_result.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    expected_output = (
        "Running service...\n"
        "[Supervisor] Restarting...\n"
        "Running service...\n"
        "[Supervisor] Restarting...\n"
        "Running service...\n"
        "[Supervisor] Restarting...\n"
        "Running service..."
    )

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == expected_output, f"Contents of {log_path} do not match expected output.\nExpected:\n{expected_output}\nActual:\n{content}"