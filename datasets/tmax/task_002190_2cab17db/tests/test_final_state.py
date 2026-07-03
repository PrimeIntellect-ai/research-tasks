# test_final_state.py

import os
import time
import subprocess
import shutil
import pytest

ARCHIVE_PATH = "/home/user/release_v2.tar.gz"
EXTRACT_DIR = "/tmp/release_test"
INPUT_WAV = "/app/release_sample.wav"
OUTPUT_WAV = "/tmp/output.wav"
BASELINE_TIME = 12.0
TARGET_SPEEDUP = 4.0

@pytest.fixture(scope="session", autouse=True)
def setup_extraction():
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    assert os.path.exists(ARCHIVE_PATH), f"Release archive not found at {ARCHIVE_PATH}"

    subprocess.run(["tar", "-xzf", ARCHIVE_PATH, "-C", EXTRACT_DIR], check=True)
    yield
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)

def test_archive_contents():
    tool_path = os.path.join(EXTRACT_DIR, "bin", "audiotool")
    lib_real = os.path.join(EXTRACT_DIR, "lib", "libaudiofilter.so.2.0.1")
    lib_sym1 = os.path.join(EXTRACT_DIR, "lib", "libaudiofilter.so.2")
    lib_sym2 = os.path.join(EXTRACT_DIR, "lib", "libaudiofilter.so")

    assert os.path.isfile(tool_path), f"Missing executable: {tool_path}"
    assert os.access(tool_path, os.X_OK), f"Not executable: {tool_path}"

    assert os.path.isfile(lib_real), f"Missing shared library: {lib_real}"

    assert os.path.islink(lib_sym1), f"Missing symlink: {lib_sym1}"
    assert os.path.islink(lib_sym2), f"Missing symlink: {lib_sym2}"

def test_execution_speedup():
    tool_path = os.path.join(EXTRACT_DIR, "bin", "audiotool")

    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = os.path.join(EXTRACT_DIR, "lib") + ":" + env.get("LD_LIBRARY_PATH", "")

    if os.path.exists(OUTPUT_WAV):
        os.remove(OUTPUT_WAV)

    start_time = time.time()
    res = subprocess.run([tool_path, INPUT_WAV, OUTPUT_WAV], env=env, capture_output=True)
    end_time = time.time()

    assert res.returncode == 0, f"Tool execution failed with return code {res.returncode}. stderr: {res.stderr.decode()}"
    assert os.path.exists(OUTPUT_WAV), "Output WAV file was not created."

    optimized_time = end_time - start_time
    assert optimized_time > 0, "Execution time must be positive."

    speedup = BASELINE_TIME / optimized_time
    assert speedup >= TARGET_SPEEDUP, f"Speedup {speedup:.2f}x is below the target threshold of {TARGET_SPEEDUP}x. (Optimized time: {optimized_time:.2f}s)"