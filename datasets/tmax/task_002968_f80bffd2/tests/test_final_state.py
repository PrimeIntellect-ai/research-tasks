# test_final_state.py
import os
import socket
import ssl
import urllib.request
import urllib.error

def test_www_directory_and_files():
    assert os.path.isdir("/home/user/www"), "/home/user/www directory is missing"

    healthz_path = "/home/user/www/healthz"
    assert os.path.isfile(healthz_path), f"{healthz_path} is missing"
    with open(healthz_path, "r") as f:
        assert f.read().strip() == "OK", f"Content of {healthz_path} is incorrect"

    metrics_path = "/home/user/www/metrics"
    assert os.path.isfile(metrics_path), f"{metrics_path} is missing"
    with open(metrics_path, "r") as f:
        assert f.read().strip() == "prometheus", f"Content of {metrics_path} is incorrect"

def test_tls_certificates():
    assert os.path.isfile("/home/user/cert.pem"), "/home/user/cert.pem is missing"
    assert os.path.isfile("/home/user/key.pem"), "/home/user/key.pem is missing"

def test_web_server_running():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8443/healthz")
        with urllib.request.urlopen(req, context=context, timeout=2) as response:
            assert response.status == 200, "Web server did not return 200 for /healthz"
            assert response.read().decode('utf-8').strip() == "OK", "Web server returned incorrect content for /healthz"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to web server on 127.0.0.1:8443: {e}"

def test_clean_paths_file():
    expected_paths = [
        "/healthz",
        "/api/v1/users",
        "/metrics",
        "/api/v2/missing"
    ]
    path_file = "/home/user/clean_paths.txt"
    assert os.path.isfile(path_file), f"{path_file} is missing"

    with open(path_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_paths, f"Content of {path_file} does not match expected paths"

def test_c_checker_files():
    assert os.path.isfile("/home/user/checker.c"), "/home/user/checker.c is missing"
    assert os.path.isfile("/home/user/checker"), "/home/user/checker executable is missing"
    assert os.access("/home/user/checker", os.X_OK), "/home/user/checker is not executable"

def test_status_report_csv():
    expected_csv = [
        "/healthz,200",
        "/api/v1/users,404",
        "/metrics,200",
        "/api/v2/missing,404"
    ]
    csv_file = "/home/user/status_report.csv"
    assert os.path.isfile(csv_file), f"{csv_file} is missing"

    with open(csv_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_csv, f"Content of {csv_file} is incorrect"