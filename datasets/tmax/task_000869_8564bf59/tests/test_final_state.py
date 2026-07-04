# test_final_state.py
import os
import time
import json
import urllib.request
import numpy as np

def test_pipeline_end_to_end():
    url = "http://localhost:8080/analyze"
    data = json.dumps({"sequence_id": "SEQ_99", "time_end": 10.0}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            assert response.status == 200, f"API returned status {response.status}"
    except Exception as e:
        assert False, f"Failed to trigger API at {url}: {e}"

    # Allow a short buffer in case file writing is slightly delayed
    time.sleep(1)

    output_file = "/home/user/output_mode_SEQ_99.txt"
    assert os.path.isfile(output_file), f"Output file not found at {output_file}. Pipeline did not generate the expected file."

    with open(output_file, "r") as f:
        content = f.read().strip()

    try:
        agent_vector = np.array([float(x.strip()) for x in content.split(",") if x.strip()])
    except ValueError:
        assert False, "Output file does not contain a valid comma-separated list of floats."

    N = len(agent_vector)
    assert N > 1, f"Generated vector is too short (length {N})."

    # For a standard 1D diffusion equation with zero Dirichlet boundary conditions,
    # the dominant spatial mode (1st left singular vector) is a half-sine wave.
    # We construct the analytical truth vector and normalize it.
    x = np.linspace(0, 1, N)
    truth_vector = np.sin(np.pi * x)

    # Normalize to match SVD output (L2 norm = 1)
    truth_vector /= np.linalg.norm(truth_vector)

    # SVD singular vectors are unique up to a sign flip (multiplication by -1)
    if np.dot(agent_vector, truth_vector) < 0:
        truth_vector = -truth_vector

    mse = np.mean((agent_vector - truth_vector)**2)

    assert mse < 1e-4, f"Metric Threshold Failed: MSE {mse:.6e} is >= 1e-4. The computed spatial mode differs significantly from the analytical ground truth."