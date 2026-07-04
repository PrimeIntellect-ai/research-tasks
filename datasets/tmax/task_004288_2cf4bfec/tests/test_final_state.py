# test_final_state.py

import os
import json
import random
import subprocess
import pytest

AGENT_EXECUTABLE = "/home/user/backup_planner"
ORACLE_EXECUTABLE = "/app/oracle_planner"
N_ITERATIONS = 50

def generate_random_vfs(seed):
    random.seed(seed)
    num_nodes = random.randint(10, 150)

    nodes = []
    dirs = ["/"]
    nodes.append({"path": "/", "type": "directory"})

    for i in range(1, num_nodes):
        parent = random.choice(dirs)
        name = f"node_{i}"
        path = f"{parent}{name}" if parent == "/" else f"{parent}/{name}"

        node_type = random.choices(["directory", "file", "symlink"], weights=[0.3, 0.6, 0.1])[0]

        # Sometimes inject paths that match EXCLUDE patterns
        if random.random() < 0.1:
            name = random.choice(["cache", "var", "log"])
            path = f"{parent}{name}" if parent == "/" else f"{parent}/{name}"
            if name == "var":
                path = "/var/log"
                node_type = "directory"

        if node_type == "directory":
            nodes.append({"path": path, "type": "directory"})
            dirs.append(path)
        elif node_type == "file":
            mtime = random.randint(1699990000, 1700010000)
            if random.random() < 0.2:
                path += ".tmp"
            nodes.append({"path": path, "type": "file", "mtime": mtime})
        else:
            target = random.choice(dirs)
            nodes.append({"path": path, "type": "symlink", "target": target})

    random.shuffle(nodes)
    return nodes

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_EXECUTABLE), f"Agent executable missing: {AGENT_EXECUTABLE}"
    assert os.access(AGENT_EXECUTABLE, os.X_OK), f"Agent executable is not executable: {AGENT_EXECUTABLE}"

@pytest.mark.parametrize("seed", range(N_ITERATIONS))
def test_fuzz_equivalence(seed):
    vfs = generate_random_vfs(seed)
    input_json = json.dumps(vfs)

    oracle_proc = subprocess.run(
        [ORACLE_EXECUTABLE],
        input=input_json,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed on seed {seed}:\n{oracle_proc.stderr}"

    agent_proc = subprocess.run(
        [AGENT_EXECUTABLE],
        input=input_json,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent failed on seed {seed}:\n{agent_proc.stderr}"

    oracle_out = oracle_proc.stdout.strip()
    agent_out = agent_proc.stdout.strip()

    if oracle_out != agent_out:
        pytest.fail(
            f"Mismatch on seed {seed}.\n"
            f"Input JSON:\n{input_json}\n\n"
            f"Oracle Output:\n{oracle_out}\n\n"
            f"Agent Output:\n{agent_out}\n"
        )