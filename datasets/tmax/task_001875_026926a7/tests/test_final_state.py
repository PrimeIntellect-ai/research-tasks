# test_final_state.py

import os
import sys
import time
import json
import urllib.request
import concurrent.futures
import pytest

def get_valid_signature(resource_id, secret):
    """
    Attempt to get the valid signature using the student's translated Python code.
    The prompt states: "The algorithm processes a resource ID and a secret to generate an expected signature."
    """
    sys.path.insert(0, '/app/flask_app')
    try:
        import crypto_utils
        # The function might take 2 arguments and return the signature
        sig = crypto_utils.validate_signature(resource_id, secret)
        if isinstance(sig, bool):
            pytest.fail("validate_signature returned a boolean instead of the expected signature string.")
        return sig
    except ImportError:
        pytest.fail("Could not import crypto_utils.py from /app/flask_app/")
    except Exception as e:
        pytest.fail(f"Error executing validate_signature: {e}")

def test_c_backend_optimized_and_fixed():
    makefile_path = "/app/c_backend/Makefile"
    assert os.path.exists(makefile_path), "Makefile is missing."

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert "-O3" in content, "Makefile does not contain the -O3 optimization flag."

    validator_path = "/app/c_backend/validator.c"
    with open(validator_path, 'r') as f:
        val_content = f.read()

    # The original delay loop was for(int i=0; i<10000000; i++)
    assert "10000000" not in val_content, "The artificial delay loop was not removed from validator.c"

def test_system_throughput_and_correctness():
    resource_id = "12345"
    secret = "SUPER_SECRET_KEY"
    sig = get_valid_signature(resource_id, secret)

    url = f"http://127.0.0.1:8080/api/v1/resource/{resource_id}?sig={sig}"

    def fetch():
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.getcode(), response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            return e.code, str(e)
        except Exception as e:
            return 0, str(e)

    num_requests = 1000
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(lambda _: fetch(), range(num_requests)))

    elapsed_time = time.time() - start_time

    successful_requests = 0
    error_samples = set()

    for status, body in results:
        if status == 200:
            try:
                data = json.loads(body)
                if "data" in data:
                    successful_requests += 1
                else:
                    error_samples.add("Response JSON missing 'data' key.")
            except json.JSONDecodeError:
                error_samples.add("Response is not valid JSON.")
        else:
            error_samples.add(f"HTTP {status}: {body[:100]}")

    throughput = successful_requests / elapsed_time if elapsed_time > 0 else 0.0

    error_msg = f"Errors encountered: {list(error_samples)[:3]}" if error_samples else ""

    assert successful_requests == num_requests, (
        f"Only {successful_requests}/{num_requests} requests succeeded. {error_msg}"
    )

    assert throughput >= 200.0, (
        f"Throughput too low: {throughput:.2f} RPS (Threshold: 200.0 RPS). "
        "Ensure the C backend delay loop is removed, compiled with -O3, and services are running concurrently."
    )