# test_final_state.py
import os
import time
import subprocess
import pytest
from pathlib import Path

def test_provision_script_execution_and_output():
    script_path = "/home/user/provision.go"
    assert os.path.exists(script_path), f"Go script missing at {script_path}"

    # Clean up images from previous runs if any to ensure fresh output
    images_dir = Path("/home/user/images")
    if images_dir.exists():
        for f in images_dir.glob("node_*.qcow2"):
            f.unlink()

    # Execute the Go script and measure time
    start_time = time.time()
    proc = subprocess.run(["go", "run", script_path], capture_output=True, text=True)
    elapsed = time.time() - start_time

    assert proc.returncode == 0, f"Go script failed with exit code {proc.returncode}. Stderr: {proc.stderr}"

    # Verify outputs
    for i in range(1, 11):
        out_file = images_dir / f"node_{i}.qcow2"
        assert out_file.exists(), f"Missing output file {out_file}"

        content = out_file.read_text().strip()
        assert content == "QCOW2_MAGIC_VALID_REPRODUCIBLE", (
            f"Invalid content in {out_file}: '{content}'. "
            "This indicates the sshd_config was not patched correctly "
            "or the required environment variables (TZ=UTC, LC_ALL=C) were not set."
        )

    # Verify metric threshold
    assert elapsed <= 3.0, f"Execution took {elapsed:.2f}s, which exceeds the 3.0s threshold. Ensure concurrency is implemented correctly."