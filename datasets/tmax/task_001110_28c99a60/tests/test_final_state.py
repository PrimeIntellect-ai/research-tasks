# test_final_state.py

import os
import json
import socket
import tarfile
import tempfile
import time
import subprocess
import requests
import pytest

def get_csv_data(legacy_data_dir):
    data = []
    for root, _, files in os.walk(legacy_data_dir):
        for file in files:
            if file.endswith(".csv"):
                with open(os.path.join(root, file), 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split(',')
                        if len(parts) == 3:
                            try:
                                data.append({
                                    "timestamp": int(parts[0]),
                                    "sensor_id": int(parts[1]),
                                    "value": float(parts[2])
                                })
                            except ValueError:
                                pass
    return data

def test_nginx_and_historical_data():
    """Test Nginx is serving the historical.tar.gz and it contains the correct data."""
    # Fetch historical.tar.gz
    try:
        response = requests.get("http://127.0.0.1:8080/historical.tar.gz", timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.fail(f"Failed to fetch historical.tar.gz from Nginx on port 8080: {e}")

    # Save and extract
    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = os.path.join(tmpdir, "historical.tar.gz")
        with open(tar_path, "wb") as f:
            f.write(response.content)

        try:
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError as e:
            pytest.fail(f"Failed to extract historical.tar.gz: {e}")

        json_path = os.path.join(tmpdir, "historical.json")
        if not os.path.exists(json_path):
            # Maybe it extracted into a subdirectory or wasn't named historical.json
            found = False
            for root, _, files in os.walk(tmpdir):
                for file in files:
                    if file == "historical.json":
                        json_path = os.path.join(root, file)
                        found = True
                        break
            if not found:
                pytest.fail("historical.json not found inside the extracted tarball.")

        with open(json_path, "r") as f:
            try:
                historical_data = json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"historical.json is not valid JSON: {e}")

    # Compare with ground truth
    expected_data = get_csv_data("/home/user/legacy_data")
    assert len(historical_data) == len(expected_data), f"Expected {len(expected_data)} records in historical.json, got {len(historical_data)}"

    # Sort both to compare
    def sort_key(x):
        return (x.get("timestamp", 0), x.get("sensor_id", 0), x.get("value", 0))

    expected_data.sort(key=sort_key)
    historical_data.sort(key=sort_key)

    for exp, act in zip(expected_data, historical_data):
        assert exp["timestamp"] == act.get("timestamp"), "Timestamp mismatch in historical data"
        assert exp["sensor_id"] == act.get("sensor_id"), "Sensor ID mismatch in historical data"
        assert abs(exp["value"] - act.get("value", 0)) < 1e-5, "Value mismatch in historical data"

def test_daemon_live_processing_and_redis():
    """Test the C daemon on port 9000, Nginx live_averages.json, and Redis integration."""
    # Connect to daemon
    try:
        s = socket.create_connection(("127.0.0.1", 9000), timeout=5)
    except OSError as e:
        pytest.fail(f"Could not connect to daemon on 127.0.0.1:9000: {e}")

    with s:
        s.settimeout(5.0)
        # Send auth
        s.sendall(b"AUTH sensor_token_99X\n")
        time.sleep(0.5)

        # Stream JSON payloads
        payloads = [
            '{"timestamp": 1700000001, "sensor_id": 1, "value": 10.0}\n',
            '{"timestamp": 1700000002, "sensor_id": 1, "value": 20.0}\n',
            '{"timestamp": 1700000003, "sensor_id": 2, "value": 15.0}\n'
        ]
        for p in payloads:
            s.sendall(p.encode('utf-8'))
            time.sleep(0.2)

    # Wait for daemon to process and write to file / redis
    time.sleep(2)

    # Fetch live_averages.json from Nginx
    try:
        response = requests.get("http://127.0.0.1:8080/live_averages.json", timeout=5)
        response.raise_for_status()
        live_averages = response.json()
    except requests.RequestException as e:
        pytest.fail(f"Failed to fetch live_averages.json from Nginx: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"live_averages.json is not valid JSON: {e}")

    # The format might be a dictionary or list, we need to extract averages for sensor 1 and 2
    # Convert to a dict for easy lookup if it's a list
    avg_dict = {}
    if isinstance(live_averages, list):
        for item in live_averages:
            sid = str(item.get("sensor_id", ""))
            if not sid:
                # maybe key is different
                continue
            avg_dict[sid] = float(item.get("average", item.get("value", 0)))
    elif isinstance(live_averages, dict):
        for k, v in live_averages.items():
            avg_dict[str(k)] = float(v)

    assert "1" in avg_dict, "Sensor 1 not found in live_averages.json"
    assert "2" in avg_dict, "Sensor 2 not found in live_averages.json"
    assert abs(avg_dict["1"] - 15.0) < 1e-5, f"Expected average for sensor 1 to be 15.0, got {avg_dict['1']}"
    assert abs(avg_dict["2"] - 15.0) < 1e-5, f"Expected average for sensor 2 to be 15.0, got {avg_dict['2']}"

    # Check Redis
    try:
        result = subprocess.run(
            ["redis-cli", "HGET", "sensor_averages", "1"],
            capture_output=True, text=True, check=True
        )
        redis_val = result.stdout.strip()
        assert redis_val != "", "Redis HGET sensor_averages 1 returned empty"
        assert abs(float(redis_val) - 15.0) < 1e-5, f"Expected Redis sensor_averages 1 to be 15.0, got {redis_val}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Redis: {e.stderr}")
    except ValueError:
        pytest.fail(f"Redis returned non-float value for sensor 1: {redis_val}")

    try:
        result = subprocess.run(
            ["redis-cli", "HGET", "sensor_averages", "2"],
            capture_output=True, text=True, check=True
        )
        redis_val = result.stdout.strip()
        assert redis_val != "", "Redis HGET sensor_averages 2 returned empty"
        assert abs(float(redis_val) - 15.0) < 1e-5, f"Expected Redis sensor_averages 2 to be 15.0, got {redis_val}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Redis: {e.stderr}")
    except ValueError:
        pytest.fail(f"Redis returned non-float value for sensor 2: {redis_val}")