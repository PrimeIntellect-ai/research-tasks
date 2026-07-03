# test_final_state.py
import os
import random
import string
import struct
import subprocess
import tempfile
import zlib
import json
import pytest

def generate_carc(seed):
    random.seed(seed)

    case_type = random.random()

    magic = b"CARC"
    if case_type < 0.1:
        magic = b"BADC"

    num_entries = random.randint(1, 20)
    paths = []
    for _ in range(num_entries):
        path_len = random.randint(1, 50)
        path = ''.join(random.choices(string.ascii_letters + string.digits, k=path_len))
        paths.append(path)

    payload = bytearray()
    for i in range(num_entries):
        path = paths[i]
        path_bytes = path.encode('utf-8')

        is_symlink = random.random() < 0.5
        if is_symlink:
            typ = 2
            target_type = random.random()
            if target_type < 0.25:
                target = random.choice(paths)
            elif target_type < 0.5:
                target = random.choice(paths)
            elif target_type < 0.75:
                target = "missing_" + ''.join(random.choices(string.ascii_letters, k=5))
            else:
                target = path
            target_bytes = target.encode('utf-8')

            payload.append(typ)
            payload.append(len(path_bytes))
            payload.extend(path_bytes)
            payload.append(len(target_bytes))
            payload.extend(target_bytes)
        else:
            typ = 1
            content_len = random.randint(1, 50)
            content = ''.join(random.choices(string.ascii_letters + string.digits, k=content_len))
            content_bytes = content.encode('utf-8')

            payload.append(typ)
            payload.append(len(path_bytes))
            payload.extend(path_bytes)
            payload.extend(struct.pack("<H", len(content_bytes)))
            payload.extend(content_bytes)

    crc = zlib.crc32(payload)
    if 0.1 <= case_type < 0.2:
        crc = crc ^ 0xFFFFFFFF

    return magic + struct.pack("<I", crc) + payload

def test_fuzz_equivalence():
    oracle_path = "/app/conf_reader"
    agent_src = "/home/user/reader.go"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_src), f"Agent code missing at {agent_src}"

    with tempfile.TemporaryDirectory() as tmpdir:
        agent_bin = os.path.join(tmpdir, "agent_bin")
        compile_res = subprocess.run(["go", "build", "-o", agent_bin, agent_src], capture_output=True, text=True)
        assert compile_res.returncode == 0, f"Agent code failed to compile:\n{compile_res.stderr}"

        for i in range(100):
            carc_data = generate_carc(i)
            input_file = os.path.join(tmpdir, f"input_{i}.carc")
            with open(input_file, "wb") as f:
                f.write(carc_data)

            oracle_out = os.path.join(tmpdir, f"oracle_out_{i}.json")
            agent_out = os.path.join(tmpdir, f"agent_out_{i}.json")

            subprocess.run([oracle_path, input_file, oracle_out], check=False)

            strace_out = os.path.join(tmpdir, f"strace_{i}.txt")
            cmd = ["strace", "-e", "trace=rename,renameat,renameat2", "-f", "-o", strace_out, agent_bin, input_file, agent_out]
            res = subprocess.run(cmd, capture_output=True, text=True)

            oracle_exists = os.path.exists(oracle_out)
            agent_exists = os.path.exists(agent_out)

            assert oracle_exists == agent_exists, f"Output file existence mismatch on input {i}. Oracle: {oracle_exists}, Agent: {agent_exists}"

            if oracle_exists:
                with open(oracle_out, "r") as f:
                    oracle_content = f.read()
                with open(agent_out, "r") as f:
                    agent_content = f.read()

                assert oracle_content == agent_content, f"Output content mismatch on input {i}.\nOracle: {oracle_content}\nAgent: {agent_content}"

                with open(strace_out, "r") as f:
                    strace_log = f.read()

                # Verify atomic rename was used
                assert "rename" in strace_log, f"Atomic rename not found in strace log for input {i}. The program must write to <out>.tmp and rename it."