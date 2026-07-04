# test_final_state.py

import os
import subprocess
import math
import socket
import struct
import json
import threading
import time
import requests
import pytest

def compute_ground_truth(video_path):
    probe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", video_path
    ]
    try:
        probe_out = subprocess.check_output(probe_cmd).decode().strip()
        width, height = map(int, probe_out.split('x'))
    except Exception as e:
        pytest.fail(f"Failed to probe video dimensions: {e}")

    cmd = [
        "ffmpeg", "-i", video_path, "-f", "image2pipe",
        "-vcodec", "rawvideo", "-pix_fmt", "gray", "-"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    count = 0
    mean_x = 0.0
    mean_y = 0.0
    m2_x = 0.0
    m2_y = 0.0

    while True:
        frame = proc.stdout.read(width * height)
        if not frame or len(frame) < width * height:
            break

        max_val = -1
        max_idx = -1
        for i, val in enumerate(frame):
            if val > max_val:
                max_val = val
                max_idx = i

        y = max_idx // width
        x = max_idx % width

        count += 1
        dx = x - mean_x
        dy = y - mean_y
        mean_x += dx / count
        mean_y += dy / count
        m2_x += dx * (x - mean_x)
        m2_y += dy * (y - mean_y)

    stddev_x = math.sqrt(m2_x / count) if count > 0 else 0.0
    stddev_y = math.sqrt(m2_y / count) if count > 0 else 0.0

    return stddev_x, stddev_y

def fetch_http(results, index):
    try:
        resp = requests.get("http://127.0.0.1:8080/latest", timeout=2)
        resp.raise_for_status()
        text = resp.text
        if "NaN" in text or "nan" in text.lower():
            results[index] = {"error": f"NaN found in response: {text}"}
            return
        data = resp.json()
        results[index] = {"data": data}
    except Exception as e:
        results[index] = {"error": str(e)}

def fetch_tcp(results, index):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("127.0.0.1", 8081))
        data = b""
        while len(data) < 32:
            chunk = s.recv(32 - len(data))
            if not chunk:
                break
            data += chunk
        s.close()
        if len(data) != 32:
            results[index] = {"error": f"Expected 32 bytes, got {len(data)}"}
            return
        x, y, stddev_x, stddev_y = struct.unpack("<dddd", data)
        if math.isnan(x) or math.isnan(y) or math.isnan(stddev_x) or math.isnan(stddev_y):
            results[index] = {"error": "NaN found in unpacked TCP data"}
            return
        results[index] = {"data": {"x": x, "y": y, "stddev_x": stddev_x, "stddev_y": stddev_y}}
    except Exception as e:
        results[index] = {"error": str(e)}

def test_service_endpoints_and_math():
    # Allow service some time to process the video and stabilize
    time.sleep(2)

    gt_stddev_x, gt_stddev_y = compute_ground_truth("/app/trajectory_test.mp4")

    num_requests = 50
    http_results = [None] * num_requests
    tcp_results = [None] * num_requests

    threads = []
    for i in range(num_requests):
        th_http = threading.Thread(target=fetch_http, args=(http_results, i))
        th_tcp = threading.Thread(target=fetch_tcp, args=(tcp_results, i))
        threads.append(th_http)
        threads.append(th_tcp)
        th_http.start()
        th_tcp.start()

    for th in threads:
        th.join()

    for i, res in enumerate(http_results):
        assert res is not None, f"HTTP request {i} did not complete"
        assert "error" not in res, f"HTTP request {i} failed: {res['error']}"
        assert "stddev_x" in res["data"], f"HTTP response missing stddev_x: {res['data']}"

    for i, res in enumerate(tcp_results):
        assert res is not None, f"TCP request {i} did not complete"
        assert "error" not in res, f"TCP request {i} failed: {res['error']}"
        assert "stddev_x" in res["data"], f"TCP response missing stddev_x: {res['data']}"

    # Check that final values match ground truth (within tolerance)
    # Using the last HTTP result as the final state
    final_http = http_results[-1]["data"]

    assert abs(final_http["stddev_x"] - gt_stddev_x) < 0.001, f"HTTP stddev_x {final_http['stddev_x']} != GT {gt_stddev_x}"
    assert abs(final_http["stddev_y"] - gt_stddev_y) < 0.001, f"HTTP stddev_y {final_http['stddev_y']} != GT {gt_stddev_y}"

    # TCP should also match ground truth
    final_tcp = tcp_results[-1]["data"]
    assert abs(final_tcp["stddev_x"] - gt_stddev_x) < 0.001, f"TCP stddev_x {final_tcp['stddev_x']} != GT {gt_stddev_x}"
    assert abs(final_tcp["stddev_y"] - gt_stddev_y) < 0.001, f"TCP stddev_y {final_tcp['stddev_y']} != GT {gt_stddev_y}"