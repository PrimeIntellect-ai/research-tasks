# test_final_state.py
import os
import time
import subprocess
import hashlib
import tempfile
import pytest

def test_validator_compiled():
    """Check if the C validator was successfully compiled."""
    validator_path = "/workspace/validator_src/validator"
    assert os.path.isfile(validator_path), f"Validator executable not found at {validator_path}. Did you fix the Makefile and build it?"
    assert os.access(validator_path, os.X_OK), f"File at {validator_path} is not executable."

def test_go_packer_speedup_and_correctness():
    """Compile the Go packer, run it against a large dataset, and compare with the oracle."""
    go_src = "/workspace/fast_packer.go"
    assert os.path.isfile(go_src), f"Go source file not found at {go_src}"

    # Compile the Go program
    go_bin = "/tmp/fast_packer"
    compile_res = subprocess.run(["go", "build", "-o", go_bin, go_src], capture_output=True, text=True)
    assert compile_res.returncode == 0, f"Go compilation failed:\n{compile_res.stderr}"
    assert os.path.isfile(go_bin), "Go binary was not created after successful compilation."

    oracle_bin = "/app/packer_oracle"
    assert os.path.isfile(oracle_bin), f"Oracle binary missing at {oracle_bin}"

    with tempfile.TemporaryDirectory() as tmpdir:
        dataset_dir = os.path.join(tmpdir, "dataset")
        os.makedirs(dataset_dir)

        # Create 10 subdirectories
        for i in range(10):
            os.makedirs(os.path.join(dataset_dir, f"dir_{i}"))

        # Generate a 500MB dataset: 10,000 files of 50KB each
        chunk = os.urandom(50 * 1024)
        for i in range(10000):
            d = os.path.join(dataset_dir, f"dir_{i % 10}")
            file_path = os.path.join(d, f"file_{i}.bin")
            with open(file_path, "wb") as f:
                # Make each file slightly unique so checksums differ
                f.write(i.to_bytes(4, 'little') + chunk[4:])

        oracle_out = os.path.join(tmpdir, "oracle.pak")
        go_out = os.path.join(tmpdir, "go.pak")

        # Run Oracle
        start_oracle = time.time()
        oracle_res = subprocess.run([oracle_bin, dataset_dir, oracle_out], capture_output=True, text=True)
        time_oracle = time.time() - start_oracle
        assert oracle_res.returncode == 0, f"Oracle failed to run:\n{oracle_res.stderr}"
        assert os.path.isfile(oracle_out), "Oracle failed to produce the output archive."

        # Run Go Packer
        start_go = time.time()
        go_res = subprocess.run([go_bin, dataset_dir, go_out], capture_output=True, text=True)
        time_go = time.time() - start_go
        assert go_res.returncode == 0, f"Go packer failed to run:\n{go_res.stderr}"
        assert os.path.isfile(go_out), "Go packer failed to produce the output archive."

        # Verify bit-for-bit identical output
        def get_sha256(path):
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for block in iter(lambda: f.read(65536), b""):
                    h.update(block)
            return h.hexdigest()

        oracle_hash = get_sha256(oracle_out)
        go_hash = get_sha256(go_out)
        assert oracle_hash == go_hash, (
            f"Output mismatch! The Go packer output does not match the Oracle output.\n"
            f"Oracle SHA256: {oracle_hash}\n"
            f"Go SHA256:     {go_hash}"
        )

        # Verify speedup metric
        speedup = time_oracle / time_go
        assert speedup >= 2.5, (
            f"Performance metric failed: Speedup is {speedup:.2f}x (Oracle: {time_oracle:.2f}s, Go: {time_go:.2f}s). "
            f"Required speedup is >= 2.5x. Ensure you are using concurrency effectively."
        )