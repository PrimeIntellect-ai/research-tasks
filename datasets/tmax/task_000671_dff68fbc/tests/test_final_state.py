# test_final_state.py

import os
import re
import subprocess
import pytest

def test_bug_fixed():
    """Test that the deliberate performance perturbation is removed."""
    consumer_path = "/app/huey-src/huey/consumer.py"
    assert os.path.isfile(consumer_path), f"{consumer_path} is missing."
    with open(consumer_path, "r") as f:
        content = f.read()
    assert "time.sleep(0.1)" not in content, "The deliberate performance perturbation 'time.sleep(0.1)' is still present in consumer.py."

def test_app_py_exists():
    """Test that app.py is created and contains expected definitions."""
    app_path = "/home/user/app.py"
    assert os.path.isfile(app_path), f"{app_path} is missing."
    with open(app_path, "r") as f:
        content = f.read()
    assert "SqliteHuey" in content, "SqliteHuey is not used in app.py."
    assert "process_data" in content, "process_data task is not defined in app.py."
    assert "huey.db" in content, "huey.db is not referenced in app.py."

def test_systemd_service_file():
    """Test that the systemd service file is created with correct configurations."""
    service_path = "/home/user/.config/systemd/user/huey-worker.service"
    assert os.path.isfile(service_path), f"Systemd service file {service_path} is missing."
    with open(service_path, "r") as f:
        content = f.read()
    assert "huey_consumer.py" in content, "huey_consumer.py is not executed in the service file."
    assert "app.huey" in content, "app.huey is not targeted in the service file."
    assert "Restart=always" in content, "Restart policy is not set to always."
    assert "RestartSec=3" in content or "RestartSec=3s" in content, "Restart delay is not set to 3 seconds."
    assert re.search(r'(-w\s*4|--workers\s*=?\s*4)', content), "Worker count is not set to 4."

def test_systemd_service_active():
    """Test that the systemd service is active and running."""
    try:
        # Check if the service is active
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "huey-worker.service"],
            capture_output=True,
            text=True
        )
        assert result.stdout.strip() == "active", f"huey-worker.service is not active. Output: {result.stdout.strip()}"
    except Exception as e:
        pytest.fail(f"Failed to check systemd service status: {e}")

def test_benchmark_result():
    """Test that the benchmark script output is present and the metric threshold is met."""
    result_path = "/home/user/benchmark_result.txt"
    assert os.path.isfile(result_path), f"{result_path} is missing."

    with open(result_path, "r") as f:
        content = f.read()

    match = re.search(r"Total time:\s*([0-9.]+)\s*seconds", content)
    if match:
        processing_time = float(match.group(1))
        assert processing_time <= 4.0, f"Processing time {processing_time} exceeded 4.0 seconds threshold."
    else:
        raise AssertionError(f"Could not find 'Total time:' metric in {result_path}")