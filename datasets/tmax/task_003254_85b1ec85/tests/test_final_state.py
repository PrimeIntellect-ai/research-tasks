# test_final_state.py
import os
import sqlite3
import subprocess
import json
import pytest
import requests

def test_recovered_db():
    db_path = "/home/user/video_service/data/recovered.db"
    assert os.path.isfile(db_path), f"Recovered database not found at {db_path}"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='video_stats';")
        table = cursor.fetchone()
        assert table is not None, "Table 'video_stats' not found in recovered.db"
        conn.close()
    except sqlite3.DatabaseError as e:
        pytest.fail(f"Recovered file is not a valid SQLite database: {e}")

def test_http_health():
    try:
        response = requests.get("http://127.0.0.1:8080/health", timeout=5)
        assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
        data = response.json()
        assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP GET /health failed: {e}")

def test_http_metrics_unauthorized():
    try:
        response = requests.get("http://127.0.0.1:8080/metrics", timeout=5)
        assert response.status_code == 401, f"Expected status 401 for unauthorized request, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP GET /metrics failed: {e}")

def test_http_metrics_authorized():
    try:
        headers = {"Authorization": "Bearer secret-uptime-token-99"}
        response = requests.get("http://127.0.0.1:8080/metrics", headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected status 200 for authorized request, got {response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"HTTP GET /metrics (authorized) failed: {e}")

def test_grpc_frame_count():
    # Calculate ground truth frame count
    video_path = "/app/incident.mp4"
    assert os.path.isfile(video_path), f"Video file {video_path} missing"

    try:
        ffprobe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-count_packets", "-show_entries", "stream=nb_read_packets",
            "-of", "csv=p=0", video_path
        ]
        result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
        expected_count = int(result.stdout.strip())
    except Exception as e:
        pytest.fail(f"Failed to calculate ground truth frame count: {e}")

    # Call gRPC service using grpcurl
    proto_dir = "/home/user/video_service/proto"
    proto_file = "video.proto"

    try:
        grpcurl_cmd = [
            "grpcurl", "-plaintext",
            "-import-path", proto_dir,
            "-proto", proto_file,
            "127.0.0.1:50051",
            "video.VideoService/GetFrameCount"
        ]
        grpc_result = subprocess.run(grpcurl_cmd, capture_output=True, text=True, timeout=10)
        assert grpc_result.returncode == 0, f"gRPC call failed: {grpc_result.stderr}"

        response_data = json.loads(grpc_result.stdout)
        actual_count = int(response_data.get("count", -1))
        assert actual_count == expected_count, f"Expected frame count {expected_count}, got {actual_count}"
    except FileNotFoundError:
        pytest.skip("grpcurl not found, skipping gRPC test")
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse gRPC response: {grpc_result.stdout}")
    except subprocess.TimeoutExpired:
        pytest.fail("gRPC call timed out")