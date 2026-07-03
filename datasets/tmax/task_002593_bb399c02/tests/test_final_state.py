# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_supervisor_installed():
    """Verify tinysupervisor was built and installed to the correct location."""
    path = "/home/user/local/bin/tinysupervisor"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did the installation fail or go to the wrong path?"
    assert os.access(path, os.X_OK), f"File {path} exists but is not executable."

def test_git_bare_repo():
    """Verify the deploy.git directory is a bare git repository."""
    path = "/home/user/deploy.git"
    assert os.path.isdir(path), f"Directory {path} does not exist."

    config_path = os.path.join(path, "config")
    assert os.path.isfile(config_path), f"Git config file {config_path} missing. Is it a valid git repo?"

    with open(config_path, "r") as f:
        content = f.read()

    assert "bare = true" in content.lower(), f"Repository at {path} is not configured as a bare repository."

def test_symlink_exists():
    """Verify the pre-receive hook is correctly symlinked to the validator script."""
    link_path = "/home/user/deploy.git/hooks/pre-receive"
    target_path = "/home/user/validate_manifest.sh"

    assert os.path.islink(link_path), f"{link_path} is not a symlink."
    actual_target = os.readlink(link_path)
    assert actual_target == target_path, f"Symlink {link_path} points to {actual_target}, expected {target_path}."

def generate_fuzz_lines(n=2000):
    """Generate a mix of valid and invalid CSV inputs based on the spec."""
    random.seed(42)
    lines = []
    chars = string.ascii_letters + string.digits + "-,:/!@#$%^&*()"

    for _ in range(n):
        if random.random() < 0.2:
            # Generate a strictly valid line
            svc = "svc-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(1, 10)))
            replicas = str(random.randint(1, 9))
            port = str(random.randint(8000, 8099))
            img = "registry.local/" + "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(1, 20))) + ":v" + str(random.randint(0, 9))
            lines.append(f"{svc},{replicas},{port},{img}")
        else:
            # Generate an invalid line (random length 5 to 150)
            length = random.randint(5, 150)
            lines.append("".join(random.choices(chars, k=length)))

    return lines

def test_fuzz_equivalence():
    """Run fuzz equivalence testing between the oracle and the agent's script."""
    oracle = "/opt/oracle/validate_manifest_oracle.sh"
    agent = "/home/user/validate_manifest.sh"

    assert os.path.isfile(agent), f"Agent script {agent} is missing."
    assert os.access(agent, os.X_OK), f"Agent script {agent} is not executable."

    lines = generate_fuzz_lines(2000)
    input_data = "\n".join(lines) + "\n"

    oracle_proc = subprocess.run([oracle], input=input_data, text=True, capture_output=True)
    agent_proc = subprocess.run([agent], input=input_data, text=True, capture_output=True)

    assert oracle_proc.returncode == 0 or agent_proc.returncode == oracle_proc.returncode, "Agent script returned a different exit code than the oracle."

    oracle_out = oracle_proc.stdout.splitlines()
    agent_out = agent_proc.stdout.splitlines()

    assert len(oracle_out) == len(agent_out), f"Output line count mismatch. Oracle produced {len(oracle_out)} lines, Agent produced {len(agent_out)} lines."

    for i, (o, a) in enumerate(zip(oracle_out, agent_out)):
        assert o == a, (
            f"Mismatch on input line {i+1}:\n"
            f"Input:  {repr(lines[i])}\n"
            f"Oracle: {o}\n"
            f"Agent:  {a}\n"
        )