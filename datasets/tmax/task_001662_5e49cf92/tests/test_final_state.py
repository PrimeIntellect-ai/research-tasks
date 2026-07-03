# test_final_state.py

import os
import re
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/project"

def test_directories_created():
    expected_dirs = ["C_src", "Python_src", "build", "config"]
    for d in expected_dirs:
        dir_path = os.path.join(PROJECT_DIR, d)
        assert os.path.isdir(dir_path), f"Directory {dir_path} was not created."

def test_files_moved():
    c_file = os.path.join(PROJECT_DIR, "C_src", "prime_c.c")
    py_file = os.path.join(PROJECT_DIR, "Python_src", "prime_py.py")

    assert os.path.isfile(c_file), f"{c_file} is missing. Did you move prime_c.c?"
    assert os.path.isfile(py_file), f"{py_file} is missing. Did you move prime_py.py?"

    assert not os.path.exists(os.path.join(PROJECT_DIR, "prime_c.c")), "prime_c.c should not be in the root directory."
    assert not os.path.exists(os.path.join(PROJECT_DIR, "prime_py.py")), "prime_py.py should not be in the root directory."

def test_shared_library_compiled():
    so_file = os.path.join(PROJECT_DIR, "build", "libprime.so")
    assert os.path.isfile(so_file), f"Shared library {so_file} is missing."

def test_benchmark_script_exists():
    bench_file = os.path.join(PROJECT_DIR, "Python_src", "benchmark.py")
    assert os.path.isfile(bench_file), f"Benchmark script {bench_file} is missing."

def test_report_file_format():
    report_file = os.path.join(PROJECT_DIR, "build", "report.txt")
    assert os.path.isfile(report_file), f"Report file {report_file} is missing."

    with open(report_file, "r") as f:
        content = f.read().strip()

    assert re.search(r"C_avg:\s*\d+(\.\d+)?(e-\d+)?", content), "report.txt is missing a valid C_avg float."
    assert re.search(r"Py_avg:\s*\d+(\.\d+)?(e-\d+)?", content), "report.txt is missing a valid Py_avg float."
    assert re.search(r"Speedup:\s*\d+(\.\d+)?(e-\d+)?", content), "report.txt is missing a valid Speedup float."

def test_haproxy_config_exists():
    cfg_file = os.path.join(PROJECT_DIR, "config", "haproxy.cfg")
    assert os.path.isfile(cfg_file), f"HAProxy config {cfg_file} is missing."

def test_services_running_and_serving_report():
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/report.txt")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}"
            content = response.read().decode('utf-8')
            assert "C_avg:" in content and "Py_avg:" in content and "Speedup:" in content, \
                "The file served at http://127.0.0.1:8080/report.txt does not look like the expected report.txt."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to HAProxy on port 8080 or the backend server on port 9000: {e}"