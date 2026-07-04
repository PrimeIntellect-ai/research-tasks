# test_final_state.py

import os
import subprocess
import random
import struct
import hashlib
import tempfile
import pytest

def test_shared_library_compiled():
    """Verify the student compiled the shared library."""
    lib_path = "/home/user/sec_lib/libsecscan.so"
    assert os.path.isfile(lib_path), f"Shared library missing at {lib_path}"

def test_fuzz_equivalence():
    """Fuzz equivalence test comparing python script against oracle binary."""
    agent_cmd = ["python3", "/home/user/py_scanner.py"]
    oracle_cmd = ["/app/oracle_scanner"]

    assert os.path.isfile(agent_cmd[1]), f"Python script missing at {agent_cmd[1]}"
    assert os.path.isfile(oracle_cmd[0]), f"Oracle missing at {oracle_cmd[0]}"

    # Generate random inputs
    random.seed(42)
    inputs = []
    N = 1000
    for _ in range(N):
        frame_id = random.randint(-2000000000, 2000000000)
        hash_bytes = bytes([random.randint(0, 255) for _ in range(32)])
        chunk = struct.pack("<i", frame_id) + hash_bytes
        inputs.append(chunk)

    input_data = b"".join(inputs)

    # Run oracle
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app:" + env.get("LD_LIBRARY_PATH", "")
    oracle_proc = subprocess.run(
        oracle_cmd, input=input_data, capture_output=True, env=env
    )
    assert oracle_proc.returncode == 0, "Oracle failed to run"
    oracle_output = oracle_proc.stdout.decode('utf-8')

    # Run agent
    agent_env = os.environ.copy()
    agent_env["LD_LIBRARY_PATH"] = "/home/user/sec_lib:" + agent_env.get("LD_LIBRARY_PATH", "")
    agent_proc = subprocess.run(
        agent_cmd, input=input_data, capture_output=True, env=agent_env
    )
    assert agent_proc.returncode == 0, f"Python script failed: {agent_proc.stderr.decode('utf-8')}"
    agent_output = agent_proc.stdout.decode('utf-8')

    # Compare
    oracle_lines = oracle_output.strip().split('\n')
    agent_lines = agent_output.strip().split('\n')

    assert len(oracle_lines) == len(agent_lines), "Output line count mismatch"

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert o_line == a_line, f"Mismatch at item {i}. Expected: '{o_line}', Got: '{a_line}'"

def test_video_artifact():
    """Verify the video artifact analysis output."""
    output_file = "/home/user/frame142_threat.txt"
    assert os.path.isfile(output_file), f"Output file missing at {output_file}"

    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_frame:
        # Extract frame 142
        # ffmpeg frame index is 1-based or 0-based depending on usage, but select=eq(n\,142) is reliable.
        # Actually, standard way: 
        subprocess.run([
            "ffmpeg", "-y", "-i", "/app/surveillance.mp4", 
            "-vf", "select=eq(n\\,142)", "-vframes", "1", 
            tmp_frame.name
        ], capture_output=True, check=True)

        with open(tmp_frame.name, "rb") as f:
            frame_data = f.read()

        raw_hash = hashlib.sha256(frame_data).digest()

    chunk = struct.pack("<i", 142) + raw_hash

    # Run oracle to get expected truth
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app:" + env.get("LD_LIBRARY_PATH", "")
    oracle_proc = subprocess.run(
        ["/app/oracle_scanner"], input=chunk, capture_output=True, env=env
    )
    expected_output = oracle_proc.stdout.decode('utf-8').strip()

    with open(output_file, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Incorrect threat score in {output_file}. Expected '{expected_output}', got '{actual_output}'"

def test_proxy_config():
    """Verify the Nginx reverse proxy configuration."""
    conf_path = "/home/user/proxy.conf"
    assert os.path.isfile(conf_path), f"Proxy config missing at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    # Basic checks for required directives
    assert "listen" in content and "8080" in content, "Nginx config missing 'listen 8080'"
    assert "location" in content and "/scan" in content, "Nginx config missing 'location /scan'"
    assert "proxy_pass" in content and "127.0.0.1:9000" in content, "Nginx config missing 'proxy_pass' to '127.0.0.1:9000'"