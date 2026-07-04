# test_final_state.py

import os
import subprocess
import pytest

def test_shared_libraries_exist():
    """Test that the compiled shared libraries exist in the correct directory."""
    lib1 = "/home/user/libs/bin/libmagic_v1.1.5.so"
    lib2 = "/home/user/libs/bin/libmagic_v2.3.1.so"

    assert os.path.exists(lib1), f"Shared library missing: {lib1}"
    assert os.path.exists(lib2), f"Shared library missing: {lib2}"

def test_resolve_py_behavior():
    """Test that resolve.py correctly identifies the highest version >= minimum."""
    resolver_path = "/home/user/resolve.py"
    assert os.path.exists(resolver_path), f"Resolver script missing: {resolver_path}"

    target_dir = "/home/user/libs/bin"
    min_version = "2.0.0"

    result = subprocess.run(
        ["python3", resolver_path, target_dir, min_version],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"resolve.py failed with error: {result.stderr}"

    output = result.stdout.strip()
    expected_output = "/home/user/libs/bin/libmagic_v2.3.1.so"

    assert output == expected_output, f"resolve.py returned '{output}', expected '{expected_output}'"

def test_e2e_result_log():
    """Test that the end-to-end test ran successfully and produced the correct log."""
    log_path = "/home/user/result.log"
    assert os.path.exists(log_path), f"Result log missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "E2E SUCCESS: 99"
    assert content == expected_content, f"result.log contains '{content}', expected '{expected_content}'"