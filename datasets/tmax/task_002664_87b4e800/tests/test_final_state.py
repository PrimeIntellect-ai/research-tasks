# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import random
import pytest

def test_frames_extraction_and_organization():
    even_dir = "/home/user/project/frames/even/"
    odd_dir = "/home/user/project/frames/odd/"

    assert os.path.isdir(even_dir), f"Directory {even_dir} does not exist."
    assert os.path.isdir(odd_dir), f"Directory {odd_dir} does not exist."

    even_files = sorted([f for f in os.listdir(even_dir) if f.endswith('.jpg')])
    odd_files = sorted([f for f in os.listdir(odd_dir) if f.endswith('.jpg')])

    assert len(even_files) == 25, f"Expected 25 even frames, found {len(even_files)}."
    assert len(odd_files) == 25, f"Expected 25 odd frames, found {len(odd_files)}."

    # Check naming conventions
    assert 'frame_0002.jpg' in even_files, "frame_0002.jpg missing from even directory."
    assert 'frame_0001.jpg' in odd_files, "frame_0001.jpg missing from odd directory."

def test_nginx_proxy():
    # Test even frame
    url_even = "http://127.0.0.1:8080/assets/even/frame_0002.jpg"
    try:
        req = urllib.request.Request(url_even)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            content = response.read()
            assert len(content) > 0, "Empty response from nginx"

            # Verify it matches the actual file
            with open("/home/user/project/frames/even/frame_0002.jpg", "rb") as f:
                expected_content = f.read()
            assert content == expected_content, "Nginx served content does not match the actual file content."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to nginx at {url_even}: {e}")

    # Test odd frame
    url_odd = "http://127.0.0.1:8080/assets/odd/frame_0001.jpg"
    try:
        req = urllib.request.Request(url_odd)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to nginx at {url_odd}: {e}")

def test_rust_binaries_exist():
    native_bin = "/home/user/project/bin/math_filter_native"
    wasm_bin = "/home/user/project/bin/math_filter.wasm"

    assert os.path.isfile(native_bin), f"Native binary missing at {native_bin}"
    assert os.access(native_bin, os.X_OK), f"Native binary {native_bin} is not executable"

    assert os.path.isfile(wasm_bin), f"WASM binary missing at {wasm_bin}"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_math_filter"
    agent_path = "/home/user/project/bin/math_filter_native"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"

    random.seed(42)
    iterations = 1000

    for i in range(iterations):
        length = random.randint(10, 500)
        nums = [random.uniform(0.0, 255.0) for _ in range(length)]
        input_str = " ".join(f"{x:.6f}" for x in nums)

        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_path],
            input=input_str,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_out = proc_oracle.stdout.strip()

        # Run agent
        try:
            proc_agent = subprocess.run(
                [agent_path],
                input=input_str,
                text=True,
                capture_output=True,
                check=True
            )
            agent_out = proc_agent.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary crashed on fuzz input {i}. Error: {e.stderr}")

        assert agent_out == oracle_out, (
            f"Mismatch on fuzz iteration {i}.\n"
            f"Input length: {length}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )