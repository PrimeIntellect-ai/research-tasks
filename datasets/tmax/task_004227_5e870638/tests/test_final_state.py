# test_final_state.py
import os
import base64
import hashlib
import time
import subprocess

def test_fast_credgen_exists():
    assert os.path.exists("/home/user/fast_credgen.c"), "Source file /home/user/fast_credgen.c is missing"
    assert os.path.exists("/home/user/fast_credgen"), "Compiled binary /home/user/fast_credgen is missing"
    assert os.access("/home/user/fast_credgen", os.X_OK), "Compiled binary /home/user/fast_credgen is not executable"

def test_correctness():
    assert os.path.exists("/home/user/rotated_creds.txt"), "Output file /home/user/rotated_creds.txt is missing"

    # Compute expected output based on the ground truth algorithm
    expected_lines = []
    with open("/app/seeds.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Decode base64
            decoded = base64.b64decode(line)
            # Append static salt
            combined = decoded + b"!SecR0t@t1on#"
            # Compute SHA-256 hash
            h = hashlib.sha256(combined).hexdigest()
            expected_lines.append(h)

    expected_content = "\n".join(expected_lines) + "\n"

    with open("/home/user/rotated_creds.txt", "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, "The generated credentials in /home/user/rotated_creds.txt do not match the expected output"

def test_performance():
    # Measure performance of the compiled C program
    start = time.perf_counter()
    result = subprocess.run(["/home/user/fast_credgen", "/app/seeds.txt", "/tmp/test_out.txt"], capture_output=True)
    duration = time.perf_counter() - start

    assert result.returncode == 0, f"fast_credgen failed with return code {result.returncode}\nStderr: {result.stderr.decode()}"

    # Verify the output produced during the performance test is also correct
    assert os.path.exists("/tmp/test_out.txt"), "fast_credgen did not create the output file during the performance test"

    with open("/tmp/test_out.txt", "r") as f:
        actual_test_content = f.read()

    with open("/home/user/rotated_creds.txt", "r") as f:
        expected_test_content = f.read()

    assert actual_test_content == expected_test_content, "The generated credentials during the performance test do not match the expected output"

    # Check against the 0.25 seconds threshold
    assert duration <= 0.25, f"Execution time {duration:.4f}s exceeded the 0.25s threshold"