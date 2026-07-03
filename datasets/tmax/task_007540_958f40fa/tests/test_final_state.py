# test_final_state.py
import os
import sys

WORKSPACE_DIR = "/home/user/workspace"
APP_DIR = os.path.join(WORKSPACE_DIR, "app")
LOG_FILE = os.path.join(WORKSPACE_DIR, "test_results.log")
NGINX_CONF = os.path.join(WORKSPACE_DIR, "nginx.conf")
ALGORITHMS_PY = os.path.join(APP_DIR, "algorithms.py")

def test_test_results_log_success():
    """Check that the integration tests were run and passed."""
    assert os.path.isfile(LOG_FILE), f"Missing file: {LOG_FILE}. Did you run the tests and redirect output?"
    with open(LOG_FILE, "r") as f:
        content = f.read()
    assert "1 passed" in content or "100%" in content, "Integration tests did not pass according to test_results.log. Ensure the tests pass and output is redirected."

def test_nginx_conf_fixed():
    """Check that nginx.conf has been modified to fix the query parameter stripping issue."""
    assert os.path.isfile(NGINX_CONF), f"Missing file: {NGINX_CONF}"
    with open(NGINX_CONF, "r") as f:
        content = f.read()

    # The original buggy line was exactly `proxy_pass http://127.0.0.1:5000/api/v1/graph;`
    # It strips query parameters. The fix could be removing the URI or adding $is_args$args.
    assert "proxy_pass http://127.0.0.1:5000/api/v1/graph;" not in content, (
        "nginx.conf still contains the buggy proxy_pass line that strips query parameters."
    )

def test_algorithms_py_fixed_import():
    """Check that the circular import has been removed from algorithms.py."""
    assert os.path.isfile(ALGORITHMS_PY), f"Missing file: {ALGORITHMS_PY}"
    with open(ALGORITHMS_PY, "r") as f:
        content = f.read()

    # Check that 'import main' is removed
    assert "import main" not in content, "algorithms.py still contains the circular 'import main'."

def test_critical_path_implementation():
    """Check that critical_path is correctly implemented and registered."""
    sys.path.insert(0, APP_DIR)
    try:
        import algorithms
    except ImportError as e:
        assert False, f"Failed to import algorithms.py: {e}"

    assert "critical_path" in algorithms.ALGORITHM_REGISTRY, "critical_path is not registered in ALGORITHM_REGISTRY."

    critical_path_func = algorithms.ALGORITHM_REGISTRY["critical_path"]

    # Test case 1: The one from the integration test
    graph1 = {
        "A": {"B": 3.0, "C": 2.0},
        "B": {"D": 4.0},
        "C": {"D": 6.0},
        "D": {}
    }
    result1 = critical_path_func(graph1, "A", "D")
    assert result1 == 8.0, f"critical_path returned {result1} for graph1, expected 8.0"

    # Test case 2: Another DAG to ensure it's not hardcoded
    graph2 = {
        "A": {"B": 1.0, "C": 10.0},
        "B": {"D": 1.0},
        "C": {"D": 1.0},
        "D": {}
    }
    result2 = critical_path_func(graph2, "A", "D")
    assert result2 == 11.0, f"critical_path returned {result2} for graph2, expected 11.0"