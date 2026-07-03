# test_final_state.py

import os
import re
import subprocess

def get_expected_key():
    crash_file = "/home/user/project/fuzz_crash.bin"
    assert os.path.isfile(crash_file), f"{crash_file} is missing"

    with open(crash_file, "rb") as f:
        data = f.read()

    match = re.search(b"APP_SECRET_KEY=([0-9a-fA-F]{32})", data)
    assert match is not None, "Could not find APP_SECRET_KEY in fuzz_crash.bin"
    return match.group(1).decode("ascii")

def test_recovered_key_file():
    expected_key = get_expected_key()
    key_file = "/home/user/recovered_key.txt"

    assert os.path.isfile(key_file), f"{key_file} is missing"

    with open(key_file, "r") as f:
        content = f.read().strip()

    assert content == expected_key, f"Expected key '{expected_key}', but found '{content}' in {key_file}"

def test_cargo_build_succeeds():
    project_dir = "/home/user/project"
    assert os.path.isdir(project_dir), f"{project_dir} is missing"

    # Run cargo build
    result = subprocess.run(
        ["cargo", "build"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cargo build failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"