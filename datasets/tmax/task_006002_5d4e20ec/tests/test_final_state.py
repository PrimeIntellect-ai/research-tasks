# test_final_state.py

import os
import sys
import json
import subprocess
import pytest

def test_scorer_translation():
    """Verify that the ReadinessScorer has been correctly translated to Python."""
    scorer_path = "/home/user/scorer.py"
    assert os.path.isfile(scorer_path), f"Missing file: {scorer_path}"

    sys.path.insert(0, "/home/user")
    try:
        import scorer
    except ImportError as e:
        pytest.fail(f"Failed to import scorer.py: {e}")

    assert hasattr(scorer, "ReadinessScorer"), "ReadinessScorer class missing in scorer.py"

    # Test the logic based on the legacy JS implementation
    window_size = 3
    s = scorer.ReadinessScorer(window_size)
    assert s.get_score() == 100, "Initial score should be 100"

    metrics = [80, 60, 50]
    for m in metrics:
        s.add_metric(m)
    assert s.get_score() == 63, f"Expected score 63, got {s.get_score()}"

    s.add_metric(30)
    assert s.get_score() == 46, f"Expected score 46, got {s.get_score()}"

    s.add_metric(90)
    assert s.get_score() == 56, f"Expected score 56, got {s.get_score()}"

    s.add_metric(10)
    assert s.get_score() == 43, f"Expected score 43, got {s.get_score()}"

def test_protobuf_files_exist():
    """Verify that the Protobuf definition and compiled files exist."""
    assert os.path.isfile("/home/user/deployment.proto"), "Missing deployment.proto"
    assert os.path.isfile("/home/user/deployment_pb2.py"), "Missing compiled deployment_pb2.py"
    assert os.path.isfile("/home/user/deployment_pb2_grpc.py"), "Missing compiled deployment_pb2_grpc.py"

def test_server_script_exists():
    """Verify that the server script exists."""
    assert os.path.isfile("/home/user/server.py"), "Missing server.py"

def test_e2e_orchestration():
    """Run the end-to-end bash script and verify it exits cleanly and creates the correct alerts.log."""
    script_path = "/home/user/run_e2e.sh"
    assert os.path.isfile(script_path), f"Missing orchestration script: {script_path}"

    alerts_log = "/home/user/alerts.log"
    if os.path.exists(alerts_log):
        os.remove(alerts_log)

    # Run the script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_e2e.sh failed with exit code {result.returncode}.\nstdout: {result.stdout}\nstderr: {result.stderr}"

    # Check if alerts.log was created
    assert os.path.isfile(alerts_log), "alerts.log was not created by the orchestration script"

    with open(alerts_log, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 alerts in alerts.log, found {len(lines)}: {lines}"

    try:
        alert1 = json.loads(lines[0])
        alert2 = json.loads(lines[1])
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON from alerts.log: {e}")

    expected_alert1 = {"alert": "deployment halted", "service": "auth-svc", "score": 46}
    expected_alert2 = {"alert": "deployment halted", "service": "payment-svc", "score": 43}

    assert alert1 == expected_alert1, f"First alert mismatch. Expected {expected_alert1}, got {alert1}"
    assert alert2 == expected_alert2, f"Second alert mismatch. Expected {expected_alert2}, got {alert2}"