# test_final_state.py

import os
import time
import subprocess
import urllib.request
import urllib.error
import concurrent.futures
import json
import pytest
import numpy as np

def wait_for_server(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(f"http://localhost:{port}/", timeout=1) as response:
                return True
        except urllib.error.URLError:
            time.sleep(0.5)
        except Exception:
            # Server might return 400/500, but it's up
            return True
    return False

def make_request():
    try:
        # Try sending the image path as a query parameter just in case it's needed
        req = urllib.request.Request("http://localhost:8080/?image=/app/reference_sample.png")
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
    except Exception as e:
        return str(e)

def test_service_memory_and_race_condition():
    service_path = "/home/user/image_service.py"
    assert os.path.exists(service_path), f"Service script not found at {service_path}"

    # Start the service
    process = subprocess.Popen(["python3", service_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for server to start
        assert wait_for_server(8080, timeout=15), "Server did not start on port 8080 within timeout."

        import psutil
        ps_process = psutil.Process(process.pid)

        num_requests = 500
        peak_memory = 0
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]

            # Monitor memory while requests are processing
            while any(not f.done() for f in futures):
                try:
                    mem_info = ps_process.memory_info()
                    rss_mb = mem_info.rss / (1024 * 1024)
                    if rss_mb > peak_memory:
                        peak_memory = rss_mb
                except psutil.NoSuchProcess:
                    break
                time.sleep(0.1)

            for f in futures:
                results.append(f.result())

        # Check memory
        assert peak_memory <= 150.0, f"PEAK_MEM_MB exceeded threshold: {peak_memory:.2f} MB > 150.0 MB. Memory leak not fixed."

        # Check for race condition / precision loss
        # Since we don't have the exact reference signature, we can verify that all successful concurrent requests 
        # returned the exact same deterministic result (MSE = 0 between responses).
        # Any race condition in a shared temp_matrix would cause variations.

        valid_results = []
        for r in results:
            if isinstance(r, dict) and 'signature' in r:
                valid_results.append(r['signature'])
            elif isinstance(r, list):
                valid_results.append(r)
            elif isinstance(r, str) and r.startswith('['):
                try:
                    valid_results.append(json.loads(r))
                except:
                    pass

        assert len(valid_results) > 0, "No valid signatures returned by the service."

        # Convert to numpy arrays
        arrays = [np.array(res, dtype=float) for res in valid_results]

        # Calculate max MSE among responses to ensure determinism
        reference = arrays[0]
        max_mse = 0.0
        for arr in arrays[1:]:
            if arr.shape != reference.shape:
                max_mse = float('inf') # Shape mismatch implies corruption
                break
            mse = np.mean((arr - reference) ** 2)
            if mse > max_mse:
                max_mse = mse

        assert max_mse <= 1e-5, f"SIGNATURE_MSE exceeded threshold: {max_mse} > 1e-5. Race condition in math operations not fixed."

    finally:
        process.terminate()
        process.wait(timeout=5)