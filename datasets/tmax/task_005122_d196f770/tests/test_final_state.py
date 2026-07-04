# test_final_state.py
import os
import subprocess
import time
import hashlib
import random
import pytest

def generate_test_data(d):
    os.makedirs(d, exist_ok=True)
    # Generate 10,000 dummy artifacts
    for i in range(10000):
        major = random.randint(0, 5)
        minor = random.randint(0, 20)
        patch = random.randint(0, 50)
        fname = f"artifact_{major}.{minor}.{patch}.bin"
        with open(os.path.join(d, fname), "wb") as f:
            f.write(os.urandom(random.randint(10, 500)))

def get_md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def test_files_exist_and_build():
    src_dir = "/home/user/src"
    c_file = os.path.join(src_dir, "fast_packer.c")
    makefile = os.path.join(src_dir, "Makefile")

    assert os.path.exists(c_file), f"Missing C source file at {c_file}"
    assert os.path.exists(makefile), f"Missing Makefile at {makefile}"

    # Build the binary
    result = subprocess.run(["make", "-C", src_dir, "all"], capture_output=True, text=True)
    assert result.returncode == 0, f"Make failed with error:\n{result.stderr}\n{result.stdout}"

    fast_bin = os.path.join(src_dir, "fast_packer")
    assert os.path.exists(fast_bin), f"Binary {fast_bin} was not created by 'make all'"
    assert os.access(fast_bin, os.X_OK), f"Binary {fast_bin} is not executable"

def test_correctness_and_speedup():
    test_dir = "/tmp/eval_data"
    generate_test_data(test_dir)

    min_v = "2.5.0"
    out_legacy = "/tmp/out_legacy.bin"
    out_fast = "/tmp/out_fast.bin"
    fast_bin = "/home/user/src/fast_packer"

    # Measure Legacy
    t0 = time.time()
    res_legacy = subprocess.run(["/app/legacy_packer", test_dir, min_v, out_legacy], capture_output=True, text=True)
    assert res_legacy.returncode == 0, f"Legacy packer failed to run:\n{res_legacy.stderr}"
    t_legacy = time.time() - t0

    # Measure Fast
    t0 = time.time()
    res_fast = subprocess.run([fast_bin, test_dir, min_v, out_fast], capture_output=True, text=True)
    assert res_fast.returncode == 0, f"Fast packer failed to run:\n{res_fast.stderr}"
    t_fast = time.time() - t0

    # Verify correctness
    assert os.path.exists(out_legacy), "Legacy packer did not produce output"
    assert os.path.exists(out_fast), "Fast packer did not produce output"

    md5_legacy = get_md5(out_legacy)
    md5_fast = get_md5(out_fast)

    assert md5_legacy == md5_fast, f"Output mismatch! Legacy MD5: {md5_legacy}, Fast MD5: {md5_fast}"

    # Verify speedup
    speedup = t_legacy / t_fast
    assert speedup >= 3.0, f"Performance requirement failed: Speedup {speedup:.2f}x is less than required 3.0x"

def test_verification_log_exists():
    log_file = "/home/user/verification.log"
    assert os.path.exists(log_file), f"Missing verification log at {log_file}"
    assert os.path.isfile(log_file), f"{log_file} is not a regular file"