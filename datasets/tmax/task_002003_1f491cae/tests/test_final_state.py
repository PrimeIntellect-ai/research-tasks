# test_final_state.py
import os
import json
import urllib.request
import subprocess
import pytest

def test_status_file():
    status_file = "/home/user/status.txt"
    assert os.path.isfile(status_file), f"Status file {status_file} not found. Did you create it?"
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert "READY" in content, f"Expected 'READY' in {status_file}, found '{content}'."

def test_api_correctness():
    url = "http://127.0.0.1:8080/api/v1/compute"
    payload = json.dumps({"values": [1.5, 2.5, 3.5, 4.5, 5.5]}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            assert "result" in data, "Response JSON missing 'result' key."
            assert abs(data["result"] - 17.5) < 1e-6, f"Expected result 17.5, got {data['result']}"
    except Exception as e:
        pytest.fail(f"Failed to communicate with API at {url}: {e}")

def test_performance_metric():
    go_code = """package main
import (
    "bytes"
    "fmt"
    "net/http"
    "sync"
    "time"
)
func main() {
    start := time.Now()
    var wg sync.WaitGroup
    payload := []byte(`{"values": [1.5, 2.5, 3.5, 4.5, 5.5]}`)
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            http.Post("http://127.0.0.1:8080/api/v1/compute", "application/json", bytes.NewBuffer(payload))
        }()
    }
    wg.Wait()
    elapsed := time.Since(start).Milliseconds()
    fmt.Println(elapsed)
}
"""
    script_path = "/tmp/eval_perf.go"
    with open(script_path, "w") as f:
        f.write(go_code)

    try:
        result = subprocess.run(["go", "run", script_path], capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, f"Go load test failed to run: {result.stderr}"

        latency_ms = int(result.stdout.strip())
        assert latency_ms <= 500, f"Metric threshold failed: latency_ms={latency_ms} > 500"
    except subprocess.TimeoutExpired:
        pytest.fail("Performance test timed out (took longer than 30s). The API is likely too slow or deadlocking.")
    except ValueError:
        pytest.fail(f"Failed to parse performance test output: {result.stdout}")
    except Exception as e:
        pytest.fail(f"Performance test execution failed: {e}")