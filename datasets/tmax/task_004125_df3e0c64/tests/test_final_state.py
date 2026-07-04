# test_final_state.py

import io
import os
import random
import subprocess
import tarfile
import pytest

def generate_random_tar(seed):
    random.seed(seed)
    num_files = random.randint(5, 50)

    out = io.BytesIO()
    with tarfile.open(fileobj=out, mode="w") as tar:
        for i in range(num_files):
            depth = random.randint(1, 4)
            path_parts = [f"dir_{random.randint(0, 5)}" for _ in range(depth - 1)]
            filename = f"file_{i}_{random.randint(0, 1000)}.dat"
            path = "/".join(path_parts + [filename]) if path_parts else filename

            size = random.randint(0, 1000)
            # Generate random bytes
            content = bytes(random.getrandbits(8) for _ in range(size))

            info = tarfile.TarInfo(name=path)
            info.size = size
            tar.addfile(info, io.BytesIO(content))

    return out.getvalue()

def test_fuzz_equivalence():
    agent_script = "/home/user/archive_tool"
    oracle_script = "/app/oracle_archive_tool"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script is not executable"

    for i in range(50):
        tar_data = generate_random_tar(seed=1000 + i)

        oracle_proc = subprocess.run(
            [oracle_script], input=tar_data, capture_output=True, text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on run {i}:\n{oracle_proc.stderr}"

        agent_proc = subprocess.run(
            [agent_script], input=tar_data, capture_output=True, text=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed (return code {agent_proc.returncode}) on run {i}:\n{agent_proc.stderr}")

        if agent_proc.stdout != oracle_proc.stdout:
            pytest.fail(
                f"Output mismatch on run {i}.\n"
                f"--- Expected Output ---\n{oracle_proc.stdout}\n"
                f"--- Agent Output ---\n{agent_proc.stdout}\n"
            )