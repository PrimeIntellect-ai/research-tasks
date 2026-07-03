# test_final_state.py

import os
import urllib.request
import urllib.error
import filecmp
import stat

def test_backup_file_exists_and_matches():
    original = "/home/user/legacy_app.log"
    backup = "/home/user/backup/legacy_app.log.bak"
    assert os.path.isfile(backup), f"Backup file {backup} does not exist."
    assert filecmp.cmp(original, backup, shallow=False), f"Backup file {backup} does not match the original {original}."

def test_rust_source_exists():
    source = "/home/user/exporter.rs"
    assert os.path.isfile(source), f"Rust source file {source} does not exist."

def test_rust_binary_exists_and_executable():
    binary = "/home/user/exporter"
    assert os.path.isfile(binary), f"Rust binary {binary} does not exist."
    assert os.access(binary, os.X_OK), f"Rust binary {binary} is not executable."

def test_run_exporter_script_exists_and_executable():
    script = "/home/user/run_exporter.sh"
    assert os.path.isfile(script), f"Automation script {script} does not exist."
    assert os.access(script, os.X_OK), f"Automation script {script} is not executable."

def test_metrics_file_content():
    metrics_file = "/home/user/metrics/metrics.txt"
    assert os.path.isfile(metrics_file), f"Metrics file {metrics_file} does not exist."

    with open(metrics_file, "r") as f:
        content = f.read().strip()

    expected_content = """# HELP legacy_app_errors Total errors
# TYPE legacy_app_errors counter
legacy_app_errors 3
# HELP legacy_app_warnings Total warnings
# TYPE legacy_app_warnings counter
legacy_app_warnings 2"""

    assert content == expected_content, f"Metrics file content does not match the expected Prometheus format.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_http_server_running_and_serving_metrics():
    url = "http://127.0.0.1:9090/metrics.txt"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}."
            content = response.read().decode('utf-8').strip()

            expected_content = """# HELP legacy_app_errors Total errors
# TYPE legacy_app_errors counter
legacy_app_errors 3
# HELP legacy_app_warnings Total warnings
# TYPE legacy_app_warnings counter
legacy_app_warnings 2"""

            assert content == expected_content, "HTTP server is not serving the correct metrics.txt content."
    except urllib.error.URLError as e:
        assert False, f"Failed to reach the HTTP server at {url}. Is it running? Error: {e}"