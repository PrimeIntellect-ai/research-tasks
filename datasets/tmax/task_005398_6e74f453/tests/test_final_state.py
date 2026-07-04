# test_final_state.py
import sys
import time
import json
import subprocess
import random
import string
import os
import pytest

def generate_url():
    data = ''.join(random.choices(string.ascii_letters, k=10))
    return f"http://example.com/api/v1/test?data={data}&chk=00"

def test_rust_library_compiled():
    # The rust library should be compiled in release mode
    lib_path = "/home/user/router_mig/validator/target/release/libvalidator.so"
    assert os.path.exists(lib_path), "Rust library was not compiled to target/release/libvalidator.so"

def test_router_module_exists():
    assert os.path.exists("/home/user/router_mig/router.py"), "router.py does not exist"

def test_router_accuracy_and_performance():
    sys.path.append('/home/user/router_mig')
    try:
        import router
    except ImportError as e:
        pytest.fail(f"Failed to import router.py: {e}")

    urls = [generate_url() for _ in range(10000)]

    # Verify correctness first (subset)
    for u in urls[:100]:
        try:
            ref_out_bytes = subprocess.check_output(['/app/ref_router', u])
            ref_out = json.loads(ref_out_bytes.decode())
        except Exception as e:
            pytest.fail(f"Failed to run /app/ref_router: {e}")

        try:
            agent_out = router.parse_and_validate(u)
        except Exception as e:
            pytest.fail(f"router.parse_and_validate failed on URL {u}: {e}")

        assert ref_out == agent_out, f"Output mismatch for URL {u}. Expected {ref_out}, got {agent_out}"

    # Benchmark
    start = time.time()
    for u in urls:
        router.parse_and_validate(u)
    end = time.time()

    duration = end - start
    assert duration <= 0.8, f"Performance requirement not met: execution took {duration:.4f} seconds, threshold is 0.8 seconds"