# test_final_state.py
import os
import csv
import requests
import concurrent.futures
import pytest

def test_results_csv_exists_and_format():
    path = "/app/results.csv"
    assert os.path.exists(path), f"Missing results file at {path}"

    with open(path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "results.csv is empty"
    assert rows[0] == ['frame', 'sum'], f"Unexpected header in results.csv: {rows[0]}"

    # 50 rows + header = 51 rows
    assert len(rows) == 51, f"Expected 51 rows (header + 50 frames) in results.csv, got {len(rows)}"

def test_plot_png_exists():
    path = "/app/plot.png"
    assert os.path.exists(path), f"Missing plot file at {path}"
    assert os.path.getsize(path) > 0, f"Plot file {path} is empty"

def test_server_endpoints():
    frames_to_test = [10, 25, 42]
    for frame in frames_to_test:
        url = f"http://localhost:9090/analyze?frame={frame}"
        try:
            response = requests.get(url, timeout=5)
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to server for frame {frame}: {e}")

        assert response.status_code == 200, f"Expected status 200 for frame {frame}, got {response.status_code}"

        try:
            val = float(response.text.strip())
        except ValueError:
            pytest.fail(f"Server response for frame {frame} is not a valid float: {response.text}")

def test_server_determinism():
    url = "http://localhost:9090/analyze?frame=15"
    num_requests = 10

    def make_request():
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.text.strip()

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                pytest.fail(f"Parallel request failed: {e}")

    assert len(results) == num_requests, "Not all requests completed successfully"

    first_result = results[0]
    for i, res in enumerate(results[1:], start=1):
        assert res == first_result, (
            f"Non-deterministic result detected! "
            f"Request 0 returned {first_result}, but Request {i} returned {res}"
        )