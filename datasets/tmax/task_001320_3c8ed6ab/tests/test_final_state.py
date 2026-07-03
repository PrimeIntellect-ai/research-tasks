# test_final_state.py
import os
import subprocess
import tempfile
import time
import re

def test_service_sh_validation():
    script = "/home/user/service.sh"
    assert os.path.isfile(script), f"Script {script} does not exist"
    assert os.access(script, os.X_OK), f"Script {script} is not executable"

    # 1. Missing arguments
    p = subprocess.run([script], capture_output=True, text=True)
    assert p.returncode == 1, "Expected exit code 1 for missing arguments"
    assert "ERROR: INVALID_REQUEST" in p.stdout, "Expected ERROR: INVALID_REQUEST for missing arguments"

    # 2. Non-existent files
    p = subprocess.run([script, "does_not_exist_1.txt", "does_not_exist_2.txt"], capture_output=True, text=True)
    assert p.returncode == 1, "Expected exit code 1 for non-existent files"
    assert "ERROR: INVALID_REQUEST" in p.stdout, "Expected ERROR: INVALID_REQUEST for non-existent files"

    # 3. Empty files
    with tempfile.NamedTemporaryFile() as f1, tempfile.NamedTemporaryFile() as f2:
        p = subprocess.run([script, f1.name, f2.name], capture_output=True, text=True)
        assert p.returncode == 1, "Expected exit code 1 for empty files"
        assert "ERROR: INVALID_REQUEST" in p.stdout, "Expected ERROR: INVALID_REQUEST for empty files"

def test_service_sh_rate_limiting():
    script = "/home/user/service.sh"

    # Create valid dummy files (size > 0)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1, tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
        f1.write("1\n")
        f2.write("1\n")
        f1_name = f1.name
        f2_name = f2.name

    try:
        # Send 3 requests, which should be allowed (they might fail internally in ffi_caller if format is wrong, but script shouldn't return 429)
        for _ in range(3):
            p = subprocess.run([script, f1_name, f2_name], capture_output=True, text=True)
            assert p.returncode != 429, "Request was rate-limited too early"

        # 4th request should be rate limited
        p4 = subprocess.run([script, f1_name, f2_name], capture_output=True, text=True)
        assert p4.returncode == 429, f"Expected exit code 429 for rate limit exceeded, got {p4.returncode}"
        assert "ERROR: RATE_LIMIT_EXCEEDED" in p4.stdout, "Expected ERROR: RATE_LIMIT_EXCEEDED in stdout"
    finally:
        os.remove(f1_name)
        os.remove(f2_name)

def test_c_library_fixes():
    so_file = "/app/libmatrix-0.1.0/libmatrix.so"
    assert os.path.isfile(so_file), f"Shared library {so_file} was not built"

    src_file = "/app/libmatrix-0.1.0/src/matrix_ops.c"
    assert os.path.isfile(src_file), f"Source file {src_file} does not exist"

    with open(src_file, "r") as f:
        content = f.read()

    # Check for out-of-bounds fix
    assert "i <=" not in content and "i <= A->rows" not in content, "Out-of-bounds array access (i <= A->rows) was not fixed"

    # Check for cache optimization (ikj or similar loop reordering)
    # The original was i, j, k. We expect k to be the middle or outer loop for the inner j loop.
    # A simple heuristic is checking if the innermost loop uses 'j' and the middle uses 'k'.
    # We will just ensure the file was modified to remove the naive i,j,k pattern.
    naive_pattern = re.compile(r"for\s*\([^)]+i\s*=\s*0.*for\s*\([^)]+j\s*=\s*0.*for\s*\([^)]+k\s*=\s*0", re.DOTALL)
    assert not naive_pattern.search(content), "Matrix multiplication loop does not appear to be optimized (still using naive i, j, k order)"