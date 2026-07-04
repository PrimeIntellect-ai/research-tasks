# test_final_state.py

import os
import subprocess
import numpy as np
import pytest

def test_output_accuracy():
    ref_path = '/app/ref_metrics.bin'
    out_path = '/home/user/metrics.bin'

    assert os.path.isfile(out_path), f"Output file {out_path} does not exist. Did you run the service and generate the metrics?"
    assert os.path.isfile(ref_path), f"Reference file {ref_path} does not exist."

    ref = np.fromfile(ref_path, dtype=np.float64)
    out = np.fromfile(out_path, dtype=np.float64)

    assert len(ref) == len(out), f"Output length {len(out)} does not match reference length {len(ref)}."

    mse = np.mean((ref - out)**2)
    assert mse <= 0.001, f"MSE {mse} is greater than threshold 0.001. The serialization logic is likely still incorrect."

def test_peak_memory_usage():
    service_dir = "/app/math-vid-service"

    # Compile the Go code
    build_cmd = ["go", "build", "-o", "math-vid-service", "."]
    result = subprocess.run(build_cmd, cwd=service_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to build Go service:\n{result.stderr}"

    # Run the service and measure memory
    run_cmd = ["/usr/bin/time", "-f", "%M", "./math-vid-service", "/app/input_video.mp4", "/tmp/test_metrics.bin"]
    result = subprocess.run(run_cmd, cwd=service_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run Go service:\n{result.stderr}"

    # Parse max_rss from the last line of stderr
    lines = result.stderr.strip().split('\n')
    max_rss_str = lines[-1].strip()
    try:
        max_rss = int(max_rss_str)
    except ValueError:
        pytest.fail(f"Could not parse max_rss from time output: {max_rss_str}")

    assert max_rss <= 60000, f"Peak memory usage {max_rss} KB exceeds threshold 60000 KB. The memory leak is not fully fixed."