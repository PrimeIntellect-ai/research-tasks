# test_final_state.py

import os
import subprocess
import pytest

def test_minimized_payload():
    min_payload_path = "/home/user/minimized_payload.bin"
    assert os.path.exists(min_payload_path), f"Minimized payload not found at {min_payload_path}"

    size = os.path.getsize(min_payload_path)
    assert size <= 6, f"Minimized payload size is {size} bytes, expected <= 6 bytes"

    orig_bin = "/tmp/orig_parser"
    assert os.path.exists("/app/parser.c"), "Original /app/parser.c is missing."

    compile_res = subprocess.run(["gcc", "-o", orig_bin, "/app/parser.c"], capture_output=True)
    assert compile_res.returncode == 0, f"Failed to compile original parser.c: {compile_res.stderr.decode('utf-8', errors='ignore')}"

    p = subprocess.run([orig_bin, min_payload_path], capture_output=True)
    # Segfault check for original binary
    assert p.returncode in (-11, 139), f"Original binary did not segfault with minimized payload. Return code: {p.returncode}"

def test_patched_parser_pass_rate():
    patched_src = "/home/user/patched_parser.c"
    assert os.path.exists(patched_src), f"Patched source not found at {patched_src}"

    patched_bin = "/tmp/patched_parser"
    compile_res = subprocess.run(["gcc", "-o", patched_bin, patched_src], capture_output=True)
    assert compile_res.returncode == 0, f"Failed to compile patched parser: {compile_res.stderr.decode('utf-8', errors='ignore')}"

    passed = 0
    total = 100

    for i in range(total):
        test_file = f"/tmp/test_{i}.bin"
        with open(test_file, "wb") as f:
            if i % 2 == 0:
                # Benign packet
                f.write(b'\x0A\x01\x00\x05' + b'B'*5)
            else:
                # Malicious packet (negative length leading to large unsigned memcpy)
                f.write(b'\x0A\x01\xff\xff' + b'C'*10)

        p = subprocess.run([patched_bin, test_file], capture_output=True)
        # Patched binary should not crash (segfault)
        if p.returncode not in (-11, 139):
            passed += 1

    pass_rate = passed / total
    assert pass_rate >= 1.0, f"Pass rate is {pass_rate}, expected 1.0 (all 100 tests must pass without segfaulting)"