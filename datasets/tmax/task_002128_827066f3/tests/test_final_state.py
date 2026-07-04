# test_final_state.py
import os
import stat
import subprocess
import time
import requests

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_csv_output():
    csv_path = "/home/user/clean_telemetry.csv"
    # If the CSV doesn't exist, try running the script to generate it
    if not os.path.exists(csv_path):
        subprocess.Popen(["/home/user/pipeline.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)

    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1700000000,t,68",
        "1700000000,h,45.5",
        "1700000001,t,72.5",
        "1700000001,h,50.0",
        "1700000002,t,23",
        "1700000002,h,80.0"
    ]

    # Check that expected lines are in the CSV (ignoring exact float formatting like 68.0 vs 68)
    # To be robust, we can parse and compare floats
    def parse_line(line):
        parts = line.split(',')
        if len(parts) == 3:
            return parts[0], parts[1], float(parts[2])
        return None

    actual_parsed = [parse_line(l) for l in lines]
    expected_parsed = [parse_line(l) for l in expected_lines]

    for exp in expected_parsed:
        assert exp in actual_parsed, f"Expected record {exp} not found in {csv_path}. Found: {actual_parsed}"

def test_http_server():
    # Ensure the script is running if the server isn't up
    try:
        requests.get("http://127.0.0.1:8080", timeout=1)
    except requests.exceptions.RequestException:
        # Start the script in the background
        subprocess.Popen(["/home/user/pipeline.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)

    try:
        response = requests.get("http://127.0.0.1:8080", timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to HTTP server on port 8080: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    body = response.text
    expected_lines = [
        "1700000000,t,68",
        "1700000000,h,45.5",
        "1700000001,t,72.5",
        "1700000001,h,50.0",
        "1700000002,t,23",
        "1700000002,h,80.0"
    ]

    # Check that expected lines are present in the response body
    for line in expected_lines:
        # We check if the basic string is in the body, or parse it to be more robust
        # Let's just check if the timestamp is there, and the metric
        parts = line.split(',')
        ts, metric, val = parts[0], parts[1], float(parts[2])

        # Look for a line matching this in the body
        found = False
        for body_line in body.splitlines():
            b_parts = body_line.strip().split(',')
            if len(b_parts) == 3 and b_parts[0] == ts and b_parts[1] == metric:
                try:
                    if abs(float(b_parts[2]) - val) < 0.1:
                        found = True
                        break
                except ValueError:
                    pass
        assert found, f"Expected record {ts},{metric},{val} not found in HTTP response body."