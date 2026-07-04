# test_final_state.py

import os
import subprocess
import re

def test_profile_exports_fstab():
    profile_path = "/home/user/.profile"
    assert os.path.isfile(profile_path), f"File {profile_path} does not exist."

    with open(profile_path, "r") as f:
        content = f.read()

    # Check for USERS_FSTAB export
    match = re.search(r'export\s+USERS_FSTAB=[\'"]?/home/user/conf/fstab[\'"]?', content)
    assert match is not None, f"USERS_FSTAB is not correctly exported in {profile_path}"

def test_crontab_entry_exists():
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True,
            check=True,
            user="user" if os.geteuid() == 0 else None
        )
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        crontab_content = ""

    # Check for * * * * * /home/user/scripts/get_socket_path > /home/user/socket_path.log
    # Allow for some whitespace variations
    pattern = r'\*\s+\*\s+\*\s+\*\s+\*\s+/home/user/scripts/get_socket_path\s+>\s+/home/user/socket_path\.log'
    assert re.search(pattern, crontab_content), "Crontab does not contain the expected cronjob entry."

def test_rust_source_exists():
    source_path = "/home/user/scripts/get_socket_path.rs"
    assert os.path.isfile(source_path), f"Rust source file {source_path} does not exist."

def test_rust_binary_exists_and_executable():
    binary_path = "/home/user/scripts/get_socket_path"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_rust_binary_output():
    binary_path = "/home/user/scripts/get_socket_path"
    env = os.environ.copy()
    env["USERS_FSTAB"] = "/home/user/conf/fstab"

    try:
        result = subprocess.run(
            [binary_path],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing {binary_path} failed with error: {e.stderr}")

    expected_output = "/home/user/run/sockets/auth.sock"
    assert output == expected_output, f"Expected output '{expected_output}', but got '{output}'"