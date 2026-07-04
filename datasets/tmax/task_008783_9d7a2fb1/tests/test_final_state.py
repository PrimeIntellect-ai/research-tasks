# test_final_state.py

import os
import subprocess
import binascii

def test_makefile_build_artifacts():
    base_dir = "/home/user/pr_review"

    lib_path = os.path.join(base_dir, "libchecksum.so")
    verifier_path = os.path.join(base_dir, "verifier")

    assert os.path.isfile(lib_path), "libchecksum.so was not built."
    assert os.path.isfile(verifier_path), "verifier executable was not built."

def test_verifier_rpath():
    base_dir = "/home/user/pr_review"
    verifier_path = os.path.join(base_dir, "verifier")

    # Check if we can run it without LD_LIBRARY_PATH
    # We'll just run it without arguments to see if it loads libraries correctly
    # If libchecksum.so is not found, it will exit with a specific error code (usually 127) or print error.
    env = os.environ.copy()
    if "LD_LIBRARY_PATH" in env:
        del env["LD_LIBRARY_PATH"]

    try:
        result = subprocess.run([verifier_path], env=env, cwd=base_dir, capture_output=True, text=True)
        # Usage error means it successfully loaded libraries and executed main
        assert "Usage:" in result.stdout or result.returncode == 1, "verifier failed to run, likely due to missing libchecksum.so (RPATH not set correctly)."
    except Exception as e:
        pytest.fail(f"Failed to execute verifier: {e}")

    # Optionally, verify with ldd
    ldd_result = subprocess.run(["ldd", verifier_path], capture_output=True, text=True)
    assert "not found" not in ldd_result.stdout, "ldd reports missing libraries, RPATH might not be set correctly."

def test_test_fixture_script():
    base_dir = "/home/user/pr_review"
    script_path = os.path.join(base_dir, "test_fixture.py")
    assert os.path.isfile(script_path), "test_fixture.py is missing."

def test_mock_data():
    base_dir = "/home/user/pr_review"
    mock_path = os.path.join(base_dir, "mock_data.bin")

    assert os.path.isfile(mock_path), "mock_data.bin is missing."
    with open(mock_path, "rb") as f:
        content = f.read()
    assert content == b"VERIFY_CHECKSUM_TEST_STRING", "mock_data.bin content is incorrect."

def test_test_result_log():
    base_dir = "/home/user/pr_review"
    log_path = os.path.join(base_dir, "test_result.log")

    assert os.path.isfile(log_path), "test_result.log is missing."

    expected_content = b"VERIFY_CHECKSUM_TEST_STRING"
    expected_crc32 = f"{binascii.crc32(expected_content) & 0xFFFFFFFF:08x}"

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    assert log_content == expected_crc32, f"test_result.log contains '{log_content}', expected '{expected_crc32}'."