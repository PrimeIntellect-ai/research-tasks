# test_final_state.py

import os
import subprocess
import time
import hashlib
import re
import pytest

def test_cpp_tool_performance():
    cpp_file = "/home/user/app/recover_pin.cpp"
    bin_file = "/home/user/app/recover_pin"

    assert os.path.exists(cpp_file), f"Missing C++ source file: {cpp_file}"

    # Compile the C++ program
    compile_proc = subprocess.run(
        ["g++", "-O3", cpp_file, "-o", bin_file],
        capture_output=True
    )
    assert compile_proc.returncode == 0, f"Compilation failed:\n{compile_proc.stderr.decode()}"

    # Generate 100 test hashes of 6-digit PINs
    test_hashes = []
    expected_pins = []
    for i in range(100):
        # We'll use 000000 to 000099 for the test batch
        pin = f"{i:06d}"
        expected_pins.append(pin)
        test_hashes.append(hashlib.sha256(pin.encode()).hexdigest())

    start_time = time.perf_counter()
    for hash_val, expected_pin in zip(test_hashes, expected_pins):
        process = subprocess.run(
            [bin_file],
            input=hash_val.encode(),
            capture_output=True
        )
        assert process.returncode == 0, f"Executable failed with return code {process.returncode}"

        output = process.stdout.decode().strip()
        assert expected_pin in output, f"Incorrect output for hash {hash_val}. Expected {expected_pin}, got {output}"

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    assert elapsed <= 0.5, f"Performance failed: {elapsed:.4f}s > 0.5s threshold"

def test_rotation_report():
    report_file = "/home/user/app/rotation_report.txt"
    assert os.path.exists(report_file), f"Missing rotation report: {report_file}"

    with open(report_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, "Rotation report must contain at least 2 lines"
    assert lines[0].strip() == "839210", f"Line 1 of rotation report should be the legacy PIN '839210', got '{lines[0]}'"
    assert len(lines[1].strip()) >= 16, "Line 2 of rotation report should be the new 16-character password"

def test_nginx_config_updated():
    nginx_conf = "/home/user/app/nginx/nginx.conf"
    assert os.path.exists(nginx_conf), f"Missing Nginx config: {nginx_conf}"

    with open(nginx_conf, "r") as f:
        content = f.read()

    assert "/auth-debug" in content, "Nginx config must reference /auth-debug/ location"
    assert "403" in content or "deny all" in content, "Nginx config must block /auth-debug/ (e.g. return 403 or deny all)"

def test_redis_config_updated():
    redis_conf = "/home/user/app/redis/redis.conf"
    assert os.path.exists(redis_conf), f"Missing Redis config: {redis_conf}"

    with open(redis_conf, "r") as f:
        content = f.read()

    # Check that requirepass is set to something
    assert re.search(r"^requirepass\s+\S+", content, flags=re.MULTILINE), "Redis config must contain 'requirepass <new_password>'"

def test_flask_env_updated():
    flask_env = "/home/user/app/flask/.env"
    assert os.path.exists(flask_env), f"Missing Flask env: {flask_env}"

    with open(flask_env, "r") as f:
        content = f.read()

    assert re.search(r"^REDIS_PASSWORD=.*", content, flags=re.MULTILINE), "Flask .env must contain REDIS_PASSWORD"