# test_final_state.py

import os
import stat
import pytest

def test_fstab_created():
    """Check if my_fstab was created with the correct content."""
    fstab_path = "/home/user/my_fstab"
    assert os.path.isfile(fstab_path), f"Missing custom fstab at {fstab_path}"

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    assert "sysfs /home/user/sys_mnt sysfs defaults 0 0" in content, "The fstab file does not contain the correct mount entry."

def test_bashrc_updated():
    """Check if .bashrc was updated with the required environment variables."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"Missing .bashrc at {bashrc_path}"

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "FSTAB_PATH=/home/user/my_fstab" in content, ".bashrc is missing FSTAB_PATH export."
    assert "STATE_DIR=/home/user/state" in content, ".bashrc is missing STATE_DIR export."

def test_rust_code_fixed():
    """Check if the Rust code was modified to read STATE_DIR from the environment."""
    main_rs_path = "/home/user/mounter/src/main.rs"
    assert os.path.isfile(main_rs_path), f"Missing main.rs at {main_rs_path}"

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "env::var(\"STATE_DIR\")" in content, "Rust code does not read STATE_DIR from the environment."
    assert "/tmp/state" not in content, "Rust code still contains the hardcoded /tmp/state directory."

def test_wrapper_script():
    """Check if start_service.sh exists, is executable, sources .bashrc, and runs the project."""
    script_path = "/home/user/start_service.sh"
    assert os.path.isfile(script_path), f"Missing wrapper script at {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    has_source = "source /home/user/.bashrc" in content or ". /home/user/.bashrc" in content
    assert has_source, "Wrapper script does not source /home/user/.bashrc."

    has_cargo = "cargo run" in content or "cargo build" in content or "mounter" in content
    assert has_cargo, "Wrapper script does not seem to build/execute the Rust project."

def test_log_created():
    """Check if the log file was created with the correct output."""
    log_path = "/home/user/state/mount_state.log"
    assert os.path.isfile(log_path), f"Missing log file at {log_path}. Did the service run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_log = "Simulated mounting sysfs on /home/user/sys_mnt"
    assert expected_log in content, f"Log file does not contain the expected message. Found: {content}"