# test_final_state.py

import os
import subprocess
import pytest

def test_run_ci_and_verify_outputs():
    # Clean up any existing artifacts directory to ensure a fresh run
    artifacts_dir = "/home/user/artifacts"
    if os.path.exists(artifacts_dir):
        subprocess.run(["rm", "-rf", artifacts_dir], check=True)

    # Run the CI script with a test commit message
    ci_script = "/home/user/run_ci.sh"
    assert os.path.exists(ci_script), f"{ci_script} does not exist."

    commit_msg = "Initial commit [ci:linux] [ci:mac]"
    result = subprocess.run(["bash", ci_script, commit_msg], capture_output=True, text=True)
    assert result.returncode == 0, f"run_ci.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Expected files and their exact contents
    expected_files = {
        "linux/base.out": "base",
        "linux/crypto.out": "crypto(base)",
        "linux/gui_x11.out": "gui_x11(base)",
        "linux/app.out": "app(base,crypto(base),gui_x11(base))",
        "mac/base.out": "base",
        "mac/gui_mac.out": "gui_mac(base)",
        "mac/app.out": "app(base,gui_mac(base))"
    }

    for rel_path, expected_content in expected_files.items():
        file_path = os.path.join(artifacts_dir, rel_path)
        assert os.path.exists(file_path), f"Expected output file missing: {file_path}"

        with open(file_path, "r") as f:
            content = f.read().strip()
            assert content == expected_content, f"Content mismatch in {file_path}. Expected '{expected_content}', got '{content}'"

def test_windows_platform_directly():
    # Test the python script directly for the windows platform
    build_manager = "/home/user/build_manager.py"
    manifest = "/home/user/manifest.json"
    assert os.path.exists(build_manager), f"{build_manager} does not exist."

    result = subprocess.run(["python3", build_manager, "--manifest", manifest, "--platform", "windows"], capture_output=True, text=True)
    assert result.returncode == 0, f"build_manager.py failed for windows.\nStderr: {result.stderr}"

    expected_files = {
        "windows/base.out": "base",
        "windows/crypto.out": "crypto(base)",
        "windows/app.out": "app(base,crypto(base))"
    }

    artifacts_dir = "/home/user/artifacts"
    for rel_path, expected_content in expected_files.items():
        file_path = os.path.join(artifacts_dir, rel_path)
        assert os.path.exists(file_path), f"Expected output file missing: {file_path}"

        with open(file_path, "r") as f:
            content = f.read().strip()
            assert content == expected_content, f"Content mismatch in {file_path}. Expected '{expected_content}', got '{content}'"