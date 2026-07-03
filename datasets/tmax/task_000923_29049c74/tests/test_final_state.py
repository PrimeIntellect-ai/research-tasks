# test_final_state.py

import os
import json
import subprocess
import pytest

def test_symlink_correct():
    symlink_path = "/home/user/libwebcrypto/libwebcrypto.so"
    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symlink, but it is not."

    target = os.readlink(symlink_path)
    expected_targets = ("libwebcrypto.so.1.3.5", "/home/user/libwebcrypto/libwebcrypto.so.1.3.5")
    assert target in expected_targets, f"Symlink points to incorrect target: {target}. Expected one of {expected_targets}."

def test_deployment_json():
    json_path = "/home/user/deployment.json"
    assert os.path.isfile(json_path), f"File {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert "libwebcrypto_version" in data, "Missing 'libwebcrypto_version' key in JSON."
    assert data["libwebcrypto_version"] == "1.3.5", f"Incorrect libwebcrypto_version: {data['libwebcrypto_version']}. Expected '1.3.5'."

    assert "regex_version" in data, "Missing 'regex_version' key in JSON."
    regex_ver = data["regex_version"]
    assert regex_ver.startswith("1.9."), f"Incorrect regex_version in JSON: {regex_ver}. Expected a 1.9.x version."

def test_cargo_build_and_run():
    tool_dir = "/home/user/web_sec_tool"
    env = os.environ.copy()
    # Add the library path so the runtime linker can find libwebcrypto.so
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"/home/user/libwebcrypto:{env['LD_LIBRARY_PATH']}"
    else:
        env["LD_LIBRARY_PATH"] = "/home/user/libwebcrypto"

    result = subprocess.run(
        ["cargo", "run"],
        cwd=tool_dir,
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"'cargo run' failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert "Encrypted value: 42" in result.stdout, "Expected output 'Encrypted value: 42' not found in cargo run output."

def test_cargo_lock_regex_version():
    lock_path = "/home/user/web_sec_tool/Cargo.lock"
    assert os.path.isfile(lock_path), f"{lock_path} is missing. Did you run 'cargo build'?"

    # Use cargo tree or pkgid to verify the actual resolved version of the regex crate
    result = subprocess.run(
        ["cargo", "pkgid", "regex"],
        cwd="/home/user/web_sec_tool",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Could not determine regex version from cargo.\nSTDERR: {result.stderr}"

    output = result.stdout.strip()
    # The output usually looks like `file:///home/user/web_sec_tool#regex@1.9.6` or similar
    assert "1.9." in output, f"Resolved regex version in Cargo does not match 1.9.x. Cargo pkgid output: {output}"