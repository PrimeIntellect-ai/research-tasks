# test_final_state.py

import os
import stat
import subprocess
import shutil
import tempfile
import pytest

def test_token_extraction():
    token_path = "/home/user/token.txt"
    assert os.path.isfile(token_path), f"Expected {token_path} to exist."

    with open(token_path, "r") as f:
        content = f.read().strip()

    expected_token = "SUPPORT-TOKEN-9X8A-2B1C-4D5E"
    assert content == expected_token, f"Expected token to be '{expected_token}', but got '{content}'."

def test_regression_executable_exists():
    regression_path = "/home/user/regression"
    assert os.path.isfile(regression_path), f"Expected {regression_path} to exist."

    st = os.stat(regression_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Expected {regression_path} to be executable."

def test_regression_behavior():
    regression_path = "/home/user/regression"
    legacy_tool_path = "/home/user/legacy_tool"

    # 1. Test that the regression test returns 0 when the bug is triggered
    result = subprocess.run([regression_path], capture_output=True)
    assert result.returncode == 0, f"Expected regression test to return 0 when bug is present, got {result.returncode}."

    # 2. Test that the regression test returns 1 when the bug is NOT triggered
    # We will temporarily replace the legacy_tool with a safe version
    backup_path = "/home/user/legacy_tool.bak"
    shutil.move(legacy_tool_path, backup_path)

    try:
        # Create a safe dummy legacy_tool
        dummy_c_path = "/home/user/dummy_safe.c"
        with open(dummy_c_path, "w") as f:
            f.write("int main() { return 0; }\n")

        subprocess.run(["gcc", "-o", legacy_tool_path, dummy_c_path], check=True)
        os.chmod(legacy_tool_path, 0o755)

        # Run regression test again
        result_safe = subprocess.run([regression_path], capture_output=True)
        assert result_safe.returncode == 1, f"Expected regression test to return 1 when bug is NOT present (tool exits 0), got {result_safe.returncode}."

    finally:
        # Restore original legacy_tool
        shutil.move(backup_path, legacy_tool_path)
        if os.path.exists("/home/user/dummy_safe.c"):
            os.remove("/home/user/dummy_safe.c")