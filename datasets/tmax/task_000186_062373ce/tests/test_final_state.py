# test_final_state.py

import time
import requests
import pytest

def test_pipeline_performance():
    """
    Test that the pipeline can process 100 cyclic jobs in under 3.0 seconds.
    This verifies that the infinite loop / OOM issue has been resolved and the services are running.
    """
    # Generate 100 jobs with a cyclic parent-child relationship
    jobs = []
    for i in range(100):
        jobs.append({
            "id": f"root_{i}",
            "value": 10,
            "children": [
                {
                    "id": f"child_{i}",
                    "value": 20,
                    "children": [
                        {
                            "id": f"root_{i}",  # Cyclic reference back to root
                            "value": 10,
                            "children": []
                        }
                    ]
                }
            ]
        })

    start = time.time()
    for i, job in enumerate(jobs):
        try:
            r = requests.post('http://127.0.0.1:5000/process', json=job, timeout=2.0)
            assert r.status_code == 200, f"Expected status 200 for job {i}, got {r.status_code}. Response: {r.text}"

            # Optionally, we can verify the sum if the API returns it, but the primary metric is duration and success.
            # A correct implementation with the cycle above should yield sum = 30 
            # (root: 10 + child: 20 + cycle_root: skipped/0)
            data = r.json()
            if "result" in data:
                assert data["result"] == 30, f"Incorrect sum calculated for job {i}: {data['result']}"

        except requests.exceptions.Timeout:
            pytest.fail(f"Request timed out on job {i}. The worker might still be caught in an infinite loop.")
        except requests.exceptions.ConnectionError:
            pytest.fail("Connection refused. Make sure the Flask API is running on port 5000.")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed on job {i}: {e}")

    duration = time.time() - start
    assert duration <= 3.0, f"Pipeline processing too slow. Took {duration:.2f} seconds, expected <= 3.0 seconds."