# test_final_state.py

import os
import subprocess
import tempfile
import random
import string
import shutil
import urllib.request
import urllib.parse
import json

def generate_random_string(length=8):
    chars = string.ascii_letters + string.digits + "_.-"
    return ''.join(random.choice(chars) for _ in range(length))

def create_random_file(path, file_type, size):
    if file_type == "text/gcode":
        with open(path, "w", encoding="utf-8") as f:
            lines = []
            current_size = 0
            while current_size < size:
                cmd = random.choice(["G0", "G1", "M104", "M109", "G28"])
                line = f"  {cmd} X{random.randint(0, 100)} Y{random.randint(0, 100)}\n"
                lines.append(line)
                current_size += len(line)
            f.write("".join(lines))
    elif file_type == "application/x-executable":
        with open(path, "wb") as f:
            f.write(b"\x7fELF" + os.urandom(max(0, size - 4)))
    else:
        with open(path, "wb") as f:
            f.write(os.urandom(size))

def generate_random_directory(base_path, max_depth, num_files):
    directories = [base_path]
    for _ in range(num_files):
        depth = random.randint(1, max_depth)
        current_dir = base_path
        for _ in range(depth - 1):
            subdir = generate_random_string(5)
            current_dir = os.path.join(current_dir, subdir)
            os.makedirs(current_dir, exist_ok=True)
            if current_dir not in directories:
                directories.append(current_dir)

        target_dir = random.choice(directories)
        filename = generate_random_string(8)
        file_type = random.choice(["text/gcode", "application/x-executable", "random_binary"])
        if file_type == "text/gcode":
            filename += ".gcode"
        elif file_type == "application/x-executable":
            filename += ".elf"
        else:
            filename += ".bin"

        filepath = os.path.join(target_dir, filename)
        size = random.randint(0, 50000)
        create_random_file(filepath, file_type, size)

def test_fuzz_equivalence():
    random.seed(42)
    oracle_bin = "/app/bin/gpak-ref"
    agent_script = "/home/user/gpak.py"

    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    for i in range(5):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = os.path.join(tmpdir, "input")
            os.makedirs(input_dir)

            num_files = random.randint(1, 20)
            generate_random_directory(input_dir, max_depth=3, num_files=num_files)

            oracle_out = os.path.join(tmpdir, "oracle.gpak")
            agent_out = os.path.join(tmpdir, "agent.gpak")

            # Run oracle
            subprocess.run([oracle_bin, "pack", oracle_out, input_dir], check=True)

            # Run agent
            res = subprocess.run(["python3", agent_script, "pack", agent_out, input_dir], capture_output=True, text=True)
            assert res.returncode == 0, f"Agent script failed:\n{res.stderr}"

            assert os.path.exists(agent_out), "Agent script did not produce output file"

            with open(oracle_out, "rb") as f:
                oracle_data = f.read()
            with open(agent_out, "rb") as f:
                agent_data = f.read()

            if oracle_data != agent_data:
                assert False, f"Output mismatch on random input directory {i}. Agent produced different bytes than oracle."

def test_end_to_end_pipeline():
    random.seed(1337)
    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        os.makedirs(input_dir)

        generate_random_directory(input_dir, max_depth=2, num_files=10)

        # Calculate expected movement lines
        expected_lines = 0
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".gcode"):
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        for line in f:
                            stripped = line.lstrip()
                            if stripped.startswith("G0") or stripped.startswith("G1"):
                                expected_lines += 1

        gpak_filename = "test_upload_123.gpak"
        gpak_path = os.path.join(tmpdir, gpak_filename)
        subprocess.run(["/app/bin/gpak-ref", "pack", gpak_path, input_dir], check=True)

        # Upload using curl to handle multipart form-data easily
        url = "http://localhost:8080/api/upload"
        res = subprocess.run(["curl", "-s", "-X", "POST", "-F", f"file=@{gpak_path}", url], capture_output=True, text=True)

        # Check Redis
        base_name = "test_upload_123"
        redis_key = f"gpak:{base_name}:movement_lines"

        redis_res = subprocess.run(["redis-cli", "get", redis_key], capture_output=True, text=True)
        assert redis_res.returncode == 0, "Failed to query redis"

        val = redis_res.stdout.strip()
        assert val != "", f"Redis key {redis_key} not found or empty"
        assert val == str(expected_lines), f"Expected {expected_lines} movement lines in Redis, got {val}"