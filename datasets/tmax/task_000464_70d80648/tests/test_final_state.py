# test_final_state.py
import os
import json
import subprocess
import random
import shutil
import zipfile

def test_transcript():
    transcript_path = "/home/user/dictation_transcript.txt"
    assert os.path.exists(transcript_path), f"Transcript missing at {transcript_path}"
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().lower()

    keywords = ["database", "password", "archive_master_2023", "rotate", "legacy"]
    missing = [kw for kw in keywords if kw not in content]
    assert not missing, f"Transcript is missing keywords: {missing}. Content: {content}"

def create_fuzz_dir(base_dir, seed):
    random.seed(seed)
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    # Create some directories
    dirs = ["", "dir1", "dir2", "dir1/subdir", "dir2/subdir2"]
    for d in dirs:
        if d:
            os.makedirs(os.path.join(base_dir, d), exist_ok=True)

    # Create text files
    for i in range(random.randint(1, 5)):
        d = random.choice(dirs)
        p = os.path.join(base_dir, d, f"file_{i}.txt")
        # Mix of ascii and iso-8859-1
        content = bytes([random.randint(32, 255) for _ in range(20)])
        with open(p, "wb") as f:
            f.write(content)

    # Create WAL files
    for i in range(random.randint(1, 3)):
        d = random.choice(dirs)
        p = os.path.join(base_dir, d, f"db_{i}.wal")
        valid = random.choice([True, False])
        if valid:
            header = b"\x37\x7f\x06\x82" + b"\x00" * 28
        else:
            header = bytes([random.randint(0, 255) for _ in range(32)])
        with open(p, "wb") as f:
            f.write(header)

    # Create zip files
    for i in range(random.randint(1, 3)):
        d = random.choice(dirs)
        p = os.path.join(base_dir, d, f"arch_{i}.zip")
        corrupted = random.choice([True, False])
        if not corrupted:
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("test.txt", "hello")
        else:
            with open(p, "wb") as f:
                f.write(b"PK\x03\x04" + b"randomgarbage")

    # Create symlinks
    for i in range(random.randint(1, 5)):
        d = random.choice(dirs)
        p = os.path.join(base_dir, d, f"link_{i}.lnk")
        loop = random.random() < 0.3
        if loop:
            # Create loop
            target = os.path.join(base_dir, random.choice(dirs))
        else:
            target = os.path.join(base_dir, random.choice(dirs), "file_0.txt")

        try:
            os.symlink(target, p)
        except FileExistsError:
            pass

def test_fuzz_equivalence():
    agent_script = "/home/user/archiver.py"
    oracle_bin = "/app/oracle_archiver"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle not found at {oracle_bin}"

    fuzz_base = "/tmp/fuzz_test_dirs"

    for i in range(50):
        test_dir = os.path.join(fuzz_base, f"test_{i}")
        create_fuzz_dir(test_dir, seed=42+i)

        # Run oracle
        oracle_proc = subprocess.run([oracle_bin, test_dir], capture_output=True, text=True)
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(["/usr/bin/python3", agent_script, test_dir], capture_output=True, text=True)
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            # Try parsing as JSON to compare structurally
            try:
                oracle_json = json.loads(oracle_out)
                agent_json = json.loads(agent_out)
                assert oracle_json == agent_json, f"JSON mismatch on iteration {i}.\nOracle: {oracle_json}\nAgent: {agent_json}"
            except json.JSONDecodeError:
                assert oracle_out == agent_out, f"Output mismatch on iteration {i}.\nOracle: {oracle_out}\nAgent: {agent_out}"