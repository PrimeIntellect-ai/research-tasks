# test_final_state.py
import os
import json
import random
import subprocess
import urllib.request
import pytest

def test_services_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
        assert "redis-server" in output, "Redis server is not running."
        assert "nginx" in output, "Nginx is not running."
        assert "gunicorn" in output, "Gunicorn is not running."
    except Exception as e:
        pytest.fail(f"Failed to check running services: {e}")

def test_libpoly_compiled():
    lib_path = "/home/user/app/c_src/libpoly.so"
    assert os.path.exists(lib_path), f"{lib_path} does not exist. Did you run make?"
    output = subprocess.check_output(["file", lib_path]).decode("utf-8")
    assert "shared object" in output, f"{lib_path} is not compiled as a shared object (-shared)."

def test_fuzz_equivalence():
    random.seed(42)
    oracle_path = "/home/user/app/reference.py"

    for _ in range(100):
        n = random.randint(10, 1000)
        m = random.randint(10, 1000)

        # Run oracle
        try:
            oracle_output = subprocess.check_output([oracle_path, str(n), str(m)]).decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed for N={n}, M={m}: {e}")

        # Run agent
        url = f"http://localhost:8080/api/merge?n={n}&m={m}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"HTTP status was {response.status} for {url}"
                agent_output = response.read().decode("utf-8").strip()
        except Exception as e:
            pytest.fail(f"Agent HTTP request failed for N={n}, M={m} via {url}: {e}")

        # Compare
        assert agent_output == oracle_output, (
            f"Mismatch for N={n}, M={m}.\n"
            f"Oracle: {oracle_output}\n"
            f"Agent:  {agent_output}"
        )

def test_redis_caching():
    n = 999
    m = 999
    url = f"http://localhost:8080/api/merge?n={n}&m={m}"

    # Make request to populate cache
    try:
        urllib.request.urlopen(url, timeout=5)
    except Exception as e:
        pytest.fail(f"Agent HTTP request failed for cache test: {e}")

    # Check redis directly
    try:
        redis_output = subprocess.check_output(["redis-cli", "get", f"poly_merge:{n}:{m}"]).decode("utf-8").strip()
        assert redis_output != "", "Redis cache is empty for the requested key."
        assert redis_output != "(nil)", f"Redis cache returned (nil) for key poly_merge:{n}:{m}."

        # The cached value should be valid JSON array
        cached_data = json.loads(redis_output)
        assert isinstance(cached_data, list), "Cached data is not a JSON list."
    except Exception as e:
        pytest.fail(f"Redis cache check failed: {e}")