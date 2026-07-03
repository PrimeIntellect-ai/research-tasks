# test_final_state.py
import os
import sys
import json
import struct
import random
import hashlib
import tempfile
import subprocess

def get_salt():
    with tempfile.TemporaryDirectory() as td:
        frame_path = os.path.join(td, "frame.png")
        subprocess.run(
            ["ffmpeg", "-y", "-i", "/app/evidence.mp4", "-ss", "00:00:05.000", "-vframes", "1", frame_path],
            check=True, capture_output=True
        )
        with open(frame_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

def create_sbk(path, files_spec, salt, bad_magic=False):
    magic = b"SBK1" if not bad_magic else b"BAD1"
    manifest = []
    data_section = bytearray()

    for spec in files_spec:
        fpath = spec["path"]
        data = spec["data"]
        bad_checksum = spec.get("bad_checksum", False)

        offset = len(data_section)
        data_section.extend(data)

        h = hashlib.sha256(data + salt.encode('utf-8')).hexdigest()
        if bad_checksum:
            h = hashlib.sha256(b"bad" + data).hexdigest()

        manifest.append({
            "path": fpath,
            "size": len(data),
            "checksum": h,
            "offset": offset
        })

    manifest_bytes = json.dumps(manifest).encode('utf-8')
    manifest_len = struct.pack("<I", len(manifest_bytes))

    with open(path, "wb") as f:
        f.write(magic)
        f.write(manifest_len)
        f.write(manifest_bytes)
        f.write(data_section)

def get_dir_state(d):
    state = {}
    for root, dirs, files in os.walk(d):
        for f in files:
            if f == ".extraction_lock":
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, d)
            with open(p, "rb") as fl:
                state[rel] = fl.read()
    return state

def test_fuzz_equivalence():
    agent_script = "/home/user/safe_extract.py"
    oracle_script = "/app/oracle_extractor.py"

    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script missing at {oracle_script}"

    salt = get_salt()
    random.seed(42)

    N = 50
    with tempfile.TemporaryDirectory() as td:
        for i in range(N):
            sbk_path = os.path.join(td, f"test_{i}.sbk")
            out_agent = os.path.join(td, f"out_agent_{i}")
            out_oracle = os.path.join(td, f"out_oracle_{i}")
            os.makedirs(out_agent, exist_ok=True)
            os.makedirs(out_oracle, exist_ok=True)

            num_files = random.randint(1, 20)
            files_spec = []
            for j in range(num_files):
                choice = random.random()
                if choice < 0.1:
                    path = f"../escaped_{j}.txt"
                elif choice < 0.2:
                    path = f"/tmp/absolute_{j}.txt"
                elif choice < 0.3:
                    path = f"valid_dir/file_{j}.txt"
                else:
                    path = f"file_{j}.txt"

                data = os.urandom(random.randint(0, 10240))
                bad_checksum = random.random() < 0.1
                files_spec.append({"path": path, "data": data, "bad_checksum": bad_checksum})

            bad_magic = random.random() < 0.05
            create_sbk(sbk_path, files_spec, salt, bad_magic)

            agent_res = subprocess.run([sys.executable, agent_script, sbk_path, out_agent, salt], capture_output=True)
            oracle_res = subprocess.run([sys.executable, oracle_script, sbk_path, out_oracle, salt], capture_output=True)

            assert agent_res.returncode == oracle_res.returncode, (
                f"Exit code mismatch on input {i}:\n"
                f"Agent exit code: {agent_res.returncode}\n"
                f"Oracle exit code: {oracle_res.returncode}\n"
                f"Agent stderr: {agent_res.stderr.decode(errors='replace')}\n"
            )

            agent_state = get_dir_state(out_agent)
            oracle_state = get_dir_state(out_oracle)

            assert agent_state.keys() == oracle_state.keys(), (
                f"Extracted files mismatch on input {i}.\n"
                f"Agent extracted: {sorted(list(agent_state.keys()))}\n"
                f"Oracle extracted: {sorted(list(oracle_state.keys()))}"
            )

            for k in agent_state:
                assert agent_state[k] == oracle_state[k], f"File content mismatch for {k} on input {i}."