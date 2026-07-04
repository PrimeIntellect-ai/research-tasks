# test_final_state.py
import pytest
import subprocess
import socket
import requests
import json

def get_green_red_status():
    cmd = [
        "ffmpeg", "-i", "/app/deploy_logs.mp4",
        "-f", "image2pipe", "-pix_fmt", "rgb24",
        "-vcodec", "rawvideo", "-"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw_video, _ = proc.communicate()

    frame_size = 100 * 100 * 3
    num_frames = len(raw_video) // frame_size

    statuses = []
    for i in range(num_frames):
        frame = raw_video[i*frame_size : (i+1)*frame_size]
        green_sum = 0
        red_sum = 0
        for y in range(10):
            for x in range(10):
                idx = (y * 100 + x) * 3
                r = frame[idx]
                g = frame[idx+1]
                red_sum += r
                green_sum += g
        statuses.append(green_sum > red_sum)
    return statuses

def parse_version(v):
    return tuple(map(int, v.split('.')))

def matches_caret(target, v):
    tv = parse_version(target)
    vv = parse_version(v)
    if vv < tv:
        return False
    if tv[0] != 0:
        return vv[0] == tv[0]
    elif tv[1] != 0:
        return vv[0] == 0 and vv[1] == tv[1]
    else:
        return vv[0] == 0 and vv[1] == 0 and vv[2] == tv[2]

@pytest.fixture(scope="module")
def truth_data():
    statuses = get_green_red_status()

    with open("/home/user/versions.txt", "r") as f:
        lines = f.read().splitlines()

    valid_versions = []
    for i, line in enumerate(lines):
        if i < len(statuses) and statuses[i]:
            parts = line.strip().split()
            if len(parts) == 2:
                valid_versions.append((parts[0], parts[1]))

    return {
        "green_count": sum(statuses),
        "valid_versions": valid_versions,
        "all_lines": lines,
        "statuses": statuses
    }

def test_tcp_status_monitor(truth_data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(("127.0.0.1", 8081))
        s.sendall(b"STATUS\n")
        data = s.recv(1024).decode()
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to communicate with TCP server on port 8081: {e}")

    expected = f"GREEN_COUNT: {truth_data['green_count']}\n"
    assert data == expected, f"TCP server returned {repr(data)}, expected {repr(expected)}"

def test_http_api_resolve_success(truth_data):
    # Find a service and target that has at least one valid version
    services = list(set([v[0] for v in truth_data["valid_versions"]]))
    if not services:
        pytest.skip("No successful versions available to test.")

    test_service = services[0]
    service_versions = [v[1] for v in truth_data["valid_versions"] if v[0] == test_service]

    # Use the lowest valid version as the target to ensure a match
    service_versions.sort(key=parse_version)
    target = f"^{service_versions[0]}"

    expected_version = None
    for v in service_versions:
        if matches_caret(service_versions[0], v):
            if expected_version is None or parse_version(v) > parse_version(expected_version):
                expected_version = v

    url = f"http://127.0.0.1:8080/deploy/resolve?service={test_service}&target={target}"
    try:
        resp = requests.get(url, timeout=2.0)
    except requests.RequestException as e:
        pytest.fail(f"HTTP GET request failed: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("service") == test_service, f"Expected service {test_service}, got {data.get('service')}"
    assert data.get("version") == expected_version, f"Expected version {expected_version}, got {data.get('version')}"

def test_http_api_resolve_not_found(truth_data):
    # Find a service and target that has NO valid versions
    # We can use a very high version constraint
    test_service = "auth-service"
    target = "^99.99.99"

    url = f"http://127.0.0.1:8080/deploy/resolve?service={test_service}&target={target}"
    try:
        resp = requests.get(url, timeout=2.0)
    except requests.RequestException as e:
        pytest.fail(f"HTTP GET request failed: {e}")

    assert resp.status_code == 404, f"Expected HTTP 404 for non-existent/invalid version, got {resp.status_code}. Response: {resp.text}"