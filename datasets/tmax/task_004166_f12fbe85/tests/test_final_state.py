# test_final_state.py
import os
import json
import urllib.request
import pytest
import numpy as np
import imageio

def get_dir_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def compute_true_error_fraction(video_path):
    try:
        reader = imageio.get_reader(video_path)
        fps = reader.get_meta_data()['fps']
    except Exception as e:
        pytest.fail(f"Failed to read video fixture {video_path}: {e}")

    red_frames = 0
    total_frames = 0

    # Approximate 1 fps extraction as requested in the prompt
    step = int(round(fps))
    if step == 0:
        step = 1

    for i, im in enumerate(reader):
        if i % step == 0:
            total_frames += 1
            # im is typically RGB
            r = im[:, :, 0]
            g = im[:, :, 1]
            b = im[:, :, 2]

            # Pure red pixels: R > 150, G < 50, B < 50
            red_mask = (r > 150) & (g < 50) & (b < 50)
            red_ratio = np.mean(red_mask)

            # Significant amount: at least 5% of the frame's pixels
            if red_ratio >= 0.05:
                red_frames += 1

    if total_frames == 0:
        return 0.0
    return red_frames / total_frames

def test_systemd_service_exists_and_configured():
    service_path = "/home/user/.config/systemd/user/monitor.service"
    assert os.path.exists(service_path), f"Systemd service file {service_path} does not exist."
    with open(service_path, "r") as f:
        content = f.read()
    assert "ExecStart=/home/user/monitor/monitor_daemon" in content, \
        "Systemd service file does not contain the correct ExecStart directive."

def test_metrics_endpoint():
    deploy_dir = "/home/user/deploy_artifacts"
    video_path = "/app/dashboard.mp4"

    true_disk_usage = get_dir_size(deploy_dir)
    true_error_fraction = compute_true_error_fraction(video_path)

    try:
        req = urllib.request.urlopen("http://127.0.0.1:9090/metrics", timeout=5)
        response_body = req.read().decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to fetch metrics from forwarded port (127.0.0.1:9090/metrics). Is the SSH tunnel and Go daemon running? Error: {e}")

    try:
        data = json.loads(response_body)
    except json.JSONDecodeError:
        pytest.fail(f"Response from metrics endpoint is not valid JSON. Got: {response_body}")

    assert "disk_usage_bytes" in data, "JSON response missing 'disk_usage_bytes' key."
    assert "error_fraction" in data, "JSON response missing 'error_fraction' key."

    agent_disk = data["disk_usage_bytes"]
    agent_err = float(data["error_fraction"])

    # Disk usage should be exactly equal (or very close if there are minor file system differences, but byte count of files is deterministic)
    assert agent_disk == true_disk_usage, \
        f"Disk usage mismatch. Expected {true_disk_usage} bytes, got {agent_disk} bytes."

    # Error fraction should be within 0.05 threshold
    abs_diff = abs(agent_err - true_error_fraction)
    assert abs_diff <= 0.05, \
        f"Error fraction mismatch. Expected ~{true_error_fraction:.4f}, got {agent_err:.4f} (difference {abs_diff:.4f} > 0.05 threshold)."