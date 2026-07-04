# test_final_state.py

import os
import subprocess
import tempfile
import shutil

def test_bare_repo_exists():
    """Check if the bare git repository is properly created."""
    repo_path = "/home/user/config-repo.git"
    assert os.path.isdir(repo_path), f"Bare repository directory {repo_path} does not exist."
    assert os.path.isdir(os.path.join(repo_path, "objects")), f"{repo_path} does not appear to be a bare git repository."

def test_validator_compiled_and_executable():
    """Check if the C validator is compiled and executable."""
    validator_path = "/home/user/sec-validator"
    assert os.path.isfile(validator_path), f"Validator executable {validator_path} does not exist."
    assert os.access(validator_path, os.X_OK), f"Validator executable {validator_path} is not executable."

def test_pre_receive_hook_exists_and_executable():
    """Check if the pre-receive hook is created and executable."""
    hook_path = "/home/user/config-repo.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"Pre-receive hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Pre-receive hook {hook_path} is not executable."

def test_validator_logic():
    """Test the compiled C validator with various inputs."""
    validator_path = "/home/user/sec-validator"

    with tempfile.TemporaryDirectory() as tmpdir:
        valid_conf = os.path.join(tmpdir, "valid.conf")
        with open(valid_conf, "w") as f:
            f.write("NETWORK_MODE=isolated\nUSER_MODE=normal\n")

        invalid1_conf = os.path.join(tmpdir, "invalid1.conf")
        with open(invalid1_conf, "w") as f:
            f.write("USER_MODE=normal\n")

        invalid2_conf = os.path.join(tmpdir, "invalid2.conf")
        with open(invalid2_conf, "w") as f:
            f.write("NETWORK_MODE=isolated\nROOT_LOGIN=true\n")

        # Test valid
        result = subprocess.run([validator_path, valid_conf], capture_output=True)
        assert result.returncode == 0, "Validator failed on a valid configuration file."

        # Test invalid 1
        result = subprocess.run([validator_path, invalid1_conf], capture_output=True)
        assert result.returncode == 1, "Validator succeeded on a configuration missing NETWORK_MODE=isolated."

        # Test invalid 2
        result = subprocess.run([validator_path, invalid2_conf], capture_output=True)
        assert result.returncode == 1, "Validator succeeded on a configuration containing ROOT_LOGIN=true."

def test_git_hook_integration():
    """Test the git pre-receive hook by simulating pushes."""
    repo_path = "/home/user/config-repo.git"

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "test-clone")

        # Clone the repo
        subprocess.run(["git", "clone", repo_path, clone_dir], check=True, capture_output=True)

        # Configure git
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=clone_dir, check=True)

        # Test valid push
        valid_conf = os.path.join(clone_dir, "valid.conf")
        with open(valid_conf, "w") as f:
            f.write("NETWORK_MODE=isolated\nUSER_MODE=normal\n")

        subprocess.run(["git", "add", "valid.conf"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add valid config"], cwd=clone_dir, check=True)

        push_valid = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
        assert push_valid.returncode == 0, "Failed to push a valid configuration file. Hook might be incorrectly rejecting it."

        # Test invalid push (missing NETWORK_MODE)
        invalid1_conf = os.path.join(clone_dir, "invalid1.conf")
        with open(invalid1_conf, "w") as f:
            f.write("USER_MODE=normal\n")

        subprocess.run(["git", "add", "invalid1.conf"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add invalid1"], cwd=clone_dir, check=True)

        push_invalid1 = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
        assert push_invalid1.returncode != 0, "Successfully pushed an invalid configuration (missing NETWORK_MODE). Hook should have rejected it."

        # Reset to test next invalid condition
        subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=clone_dir, check=True)

        # Test invalid push (has ROOT_LOGIN=true)
        invalid2_conf = os.path.join(clone_dir, "invalid2.conf")
        with open(invalid2_conf, "w") as f:
            f.write("NETWORK_MODE=isolated\nROOT_LOGIN=true\n")

        subprocess.run(["git", "add", "invalid2.conf"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add invalid2"], cwd=clone_dir, check=True)

        push_invalid2 = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
        assert push_invalid2.returncode != 0, "Successfully pushed an invalid configuration (has ROOT_LOGIN=true). Hook should have rejected it."