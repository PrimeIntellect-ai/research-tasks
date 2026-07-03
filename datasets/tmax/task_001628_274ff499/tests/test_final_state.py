# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_fuzz_equivalence():
    """Fuzz test the agent's binary against the oracle."""
    oracle_path = "/app/user_token_bin"
    agent_path = "/home/user/token_gen"

    assert os.path.exists(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable"

    random.seed(42)

    for _ in range(100):
        # Generate random inputs
        arg1_len = random.randint(3, 12)
        arg1 = ''.join(random.choices(string.ascii_lowercase, k=arg1_len))

        arg2_len = random.randint(3, 12)
        arg2 = ''.join(random.choices(string.ascii_lowercase, k=arg2_len))

        arg3 = str(random.randint(1000, 5000))

        # Run oracle
        oracle_proc = subprocess.run([oracle_path, arg1, arg2, arg3], capture_output=True, text=True)
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run([agent_path, arg1, arg2, arg3], capture_output=True, text=True)
        agent_out = agent_proc.stdout

        assert agent_proc.returncode == oracle_proc.returncode, f"Return code mismatch for inputs ({arg1}, {arg2}, {arg3}). Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        assert agent_out == oracle_out, f"Output mismatch for inputs ({arg1}, {arg2}, {arg3}). Oracle: {oracle_out!r}, Agent: {agent_out!r}"

def test_git_repository_and_hook():
    """Test the bare git repository and pre-receive hook."""
    repo_path = "/home/user/account_config.git"
    hook_path = os.path.join(repo_path, "hooks", "pre-receive")

    assert os.path.isdir(repo_path), f"Bare git repository not found at {repo_path}"
    assert os.path.isfile(os.path.join(repo_path, "HEAD")), f"{repo_path} does not appear to be a git repository"
    # Bare repo check (config should have core.bare = true, or no .git dir)
    assert not os.path.exists(os.path.join(repo_path, ".git")), f"{repo_path} should be a bare repository"

    assert os.path.exists(hook_path), f"pre-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"pre-receive hook {hook_path} is not executable"

    with open(hook_path, 'r') as f:
        hook_content = f.read()

    assert "/home/user/token_gen testuser testgroup 1000" in hook_content, "Hook does not invoke token_gen with correct arguments"
    assert "/home/user/hook_test.log" in hook_content, "Hook does not log output to /home/user/hook_test.log"

def test_setup_script():
    """Test the setup_users.sh script."""
    script_path = "/home/user/setup_users.sh"

    assert os.path.exists(script_path), f"Setup script not found at {script_path}"

    with open(script_path, 'r') as f:
        script_content = f.read()

    assert "appuser1" in script_content, "Script does not mention appuser1"
    assert "appuser2" in script_content, "Script does not mention appuser2"
    assert "appgroup" in script_content, "Script does not mention appgroup"