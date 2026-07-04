# test_final_state.py
import os
import stat
import json
import pytest

def test_files_exist():
    """Test that all required files exist."""
    required_files = [
        "/home/user/edge_parser.go",
        "/home/user/deploy.sh",
        "/home/user/filtered_logs.txt",
        "/home/user/config.json",
        "/home/user/edge_bin",
        "/home/user/metrics.out"
    ]
    for filepath in required_files:
        assert os.path.isfile(filepath), f"Required file missing: {filepath}"

def test_filtered_logs_content():
    """Test that filtered_logs.txt contains the correct extracted temperatures."""
    log_path = "/home/user/raw_sensors.log"
    filtered_path = "/home/user/filtered_logs.txt"

    assert os.path.isfile(log_path), f"Missing {log_path}"
    assert os.path.isfile(filtered_path), f"Missing {filtered_path}"

    expected_temps = []
    with open(log_path, 'r') as f:
        for line in f:
            if "CRITICAL" in line:
                # Extract temperature e.g., "Temp: 90C" -> 90
                parts = line.split()
                for part in parts:
                    if part.endswith("C") and part[:-1].isdigit():
                        expected_temps.append(part[:-1])
                        break

    with open(filtered_path, 'r') as f:
        actual_temps = [line.strip() for line in f if line.strip()]

    assert actual_temps == expected_temps, "filtered_logs.txt does not contain the correct extracted temperatures."

def test_config_json_validity():
    """Test that config.json is valid and contains correct paths."""
    config_path = "/home/user/config.json"
    assert os.path.isfile(config_path), f"Missing {config_path}"

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("config.json is not a valid JSON file.")

    assert config.get("input_file") == "/home/user/filtered_logs.txt", "config.json input_file path is incorrect."
    assert config.get("output_file") == "/home/user/metrics.out", "config.json output_file path is incorrect."

def test_permissions():
    """Test the permissions of edge_bin and metrics.out."""
    bin_path = "/home/user/edge_bin"
    out_path = "/home/user/metrics.out"

    assert os.path.isfile(bin_path), f"Missing {bin_path}"
    assert os.path.isfile(out_path), f"Missing {out_path}"

    bin_mode = stat.S_IMODE(os.stat(bin_path).st_mode)
    out_mode = stat.S_IMODE(os.stat(out_path).st_mode)

    assert bin_mode == 0o500, f"edge_bin permissions should be 0500, but got {oct(bin_mode)}"
    assert out_mode == 0o400, f"metrics.out permissions should be 0400, but got {oct(out_mode)}"

def test_metrics_out_content():
    """Test that metrics.out contains the correct average temperature."""
    filtered_path = "/home/user/filtered_logs.txt"
    out_path = "/home/user/metrics.out"

    assert os.path.isfile(filtered_path), f"Missing {filtered_path}"
    assert os.path.isfile(out_path), f"Missing {out_path}"

    with open(filtered_path, 'r') as f:
        temps = [int(line.strip()) for line in f if line.strip().isdigit()]

    assert len(temps) > 0, "No valid temperatures found in filtered_logs.txt to calculate average."

    expected_avg = sum(temps) / len(temps)
    expected_output = f"Average_Temp: {expected_avg:.2f}"

    with open(out_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"metrics.out content is incorrect. Expected '{expected_output}', got '{actual_output}'"