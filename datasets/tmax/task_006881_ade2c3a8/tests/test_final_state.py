# test_final_state.py

import os
import stat

def test_migrator_rs_exists():
    """Verify that the Rust source file was created."""
    assert os.path.isfile('/home/user/migrator.rs'), "The Rust source file /home/user/migrator.rs is missing."

def test_filesystem_structure_and_permissions():
    """Verify the exact filesystem structure, permissions, and symlinks in /home/user/new_volume."""
    base_dir = '/home/user/new_volume'
    assert os.path.isdir(base_dir), f"The target directory {base_dir} is missing."

    expected_state = {
        'configs': {'type': 'd', 'perms': 0o750},
        'configs/database.conf': {'type': 'f', 'perms': 0o600},
        'data': {'type': 'd', 'perms': 0o700},
        'data/v1': {'type': 'd', 'perms': 0o755},
        'data/active': {'type': 'l', 'target': 'v1'},
        'current_config': {'type': 'l', 'target': 'configs/database.conf'},
    }

    for path, props in expected_state.items():
        full_path = os.path.join(base_dir, path)
        assert os.path.lexists(full_path), f"Path missing: {full_path}"

        if props['type'] == 'd':
            assert os.path.isdir(full_path), f"Expected directory at {full_path}"
            mode = stat.S_IMODE(os.stat(full_path).st_mode)
            assert mode == props['perms'], f"Expected permissions {oct(props['perms'])} for {full_path}, got {oct(mode)}"
        elif props['type'] == 'f':
            assert os.path.isfile(full_path), f"Expected file at {full_path}"
            assert not os.path.islink(full_path), f"Expected regular file at {full_path}, not a symlink"
            mode = stat.S_IMODE(os.stat(full_path).st_mode)
            assert mode == props['perms'], f"Expected permissions {oct(props['perms'])} for {full_path}, got {oct(mode)}"
        elif props['type'] == 'l':
            assert os.path.islink(full_path), f"Expected symlink at {full_path}"
            target = os.readlink(full_path)
            assert target == props['target'], f"Expected symlink {full_path} to point to {props['target']}, got {target}"

def test_verification_log():
    """Verify the contents of the generated log file."""
    log_path = '/home/user/migration_verify.log'
    assert os.path.isfile(log_path), f"Verification log {log_path} is missing."

    expected_log = (
        "d configs 750\n"
        "d data 700\n"
        "d data/v1 755\n"
        "f configs/database.conf 600\n"
        "l current_config 777\n"
        "l data/active 777\n"
        "current_config -> configs/database.conf\n"
        "data/active -> v1\n"
    )

    with open(log_path, 'r') as f:
        actual_log = f.read()

    assert actual_log.strip() == expected_log.strip(), (
        f"Log file contents do not match expected.\n"
        f"Expected:\n{expected_log.strip()}\n\n"
        f"Actual:\n{actual_log.strip()}"
    )