# test_final_state.py

import os
import random
import subprocess
import pytest

def test_deployment_state():
    repo_path = "/home/user/audio_service.git"
    assert os.path.isdir(repo_path), f"Bare repository not found at {repo_path}"

    hook_path = os.path.join(repo_path, "hooks", "post-receive")
    assert os.path.isfile(hook_path), f"post-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-receive hook is not executable"

    current_symlink = "/home/user/releases/current"
    assert os.path.islink(current_symlink), f"Symlink not found at {current_symlink}"

    agent_executable = os.path.join(current_symlink, "target", "release", "audio_service")
    assert os.path.isfile(agent_executable), f"Agent executable not found at {agent_executable}"
    assert os.access(agent_executable, os.X_OK), f"Agent executable is not executable"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/audio_service_oracle"
    agent_path = "/home/user/releases/current/target/release/audio_service"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent executable not found at {agent_path}"

    random.seed(42)

    num_iterations = 1000
    for i in range(num_iterations):
        length = random.randint(0, 65536)
        input_data = random.randbytes(length)

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"

        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent executable failed with return code {agent_proc.returncode} on iteration {i} with input length {length}")

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(f"Output mismatch on iteration {i} with input length {length}. Expected {len(oracle_proc.stdout)} bytes, got {len(agent_proc.stdout)} bytes.")