# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def generate_fuzz_inputs(n):
    random.seed(42)
    chars = string.ascii_letters + string.digits + "/_"
    inputs = []
    for _ in range(n):
        length = random.randint(5, 50)
        if random.random() < 0.5:
            prefix_len = max(0, length - 10)
            prefix = ''.join(random.choice(chars) for _ in range(prefix_len))
            suffix = ''.join(random.choice(string.digits) for _ in range(6)) + ".jpg"
            inputs.append(prefix + suffix)
        else:
            inputs.append(''.join(random.choice(chars) for _ in range(length)))
    return inputs

def test_fuzz_equivalence():
    oracle_path = "/app/reference_organizer"
    agent_path = "/home/user/organizer"

    assert os.path.exists(agent_path), f"Agent program missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program is not executable: {agent_path}"

    inputs = generate_fuzz_inputs(10000)
    input_str = "\n".join(inputs) + "\n"

    oracle_proc = subprocess.run([oracle_path], input=input_str, text=True, capture_output=True)
    agent_proc = subprocess.run([agent_path], input=input_str, text=True, capture_output=True)

    assert oracle_proc.returncode == 0, "Oracle failed to run"

    oracle_lines = oracle_proc.stdout.splitlines()
    agent_lines = agent_proc.stdout.splitlines()

    assert len(oracle_lines) == len(inputs), "Oracle did not output the expected number of lines"
    assert len(agent_lines) == len(inputs), f"Agent output {len(agent_lines)} lines, expected {len(inputs)}"

    for i, (inp, o_line, a_line) in enumerate(zip(inputs, oracle_lines, agent_lines)):
        assert o_line == a_line, f"Mismatch on input {i!r}: {inp!r}\nOracle: {o_line!r}\nAgent:  {a_line!r}"

def test_dataset_extraction_and_linking():
    raw_dir = "/home/user/raw_frames"
    train_dir = "/home/user/dataset/train_set"
    val_dir = "/home/user/dataset/val_set"

    assert os.path.isdir(raw_dir), f"Raw frames directory missing: {raw_dir}"
    assert os.path.isdir(train_dir), f"Train set directory missing: {train_dir}"
    assert os.path.isdir(val_dir), f"Val set directory missing: {val_dir}"

    raw_files = sorted(os.listdir(raw_dir))
    assert len(raw_files) == 50, f"Expected 50 raw frames, found {len(raw_files)}"

    for i in range(1, 51):
        filename = f"{i:06d}.jpg"
        assert filename in raw_files, f"Missing raw frame: {filename}"

        raw_path = os.path.join(raw_dir, filename)

        if i % 5 == 0:
            val_filename = f"val_{filename}"
            val_path = os.path.join(val_dir, val_filename)
            assert os.path.exists(val_path), f"Missing validation file: {val_path}"
            assert not os.path.islink(val_path), f"Validation file should be a hardlink, not symlink: {val_path}"
            assert os.stat(val_path).st_ino == os.stat(raw_path).st_ino, f"Validation file {val_path} is not a hardlink to {raw_path}"
        else:
            train_filename = f"train_{filename}"
            train_path = os.path.join(train_dir, train_filename)
            assert os.path.islink(train_path), f"Train file should be a symlink: {train_path}"
            target = os.readlink(train_path)
            assert target == raw_path, f"Train symlink {train_path} points to {target}, expected absolute path {raw_path}"