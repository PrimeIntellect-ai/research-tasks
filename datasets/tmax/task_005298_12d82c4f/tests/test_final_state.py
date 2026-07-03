# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import subprocess
import pytest

def test_final_output_json():
    output_path = "/home/user/final_output.json"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."
    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    expected = {"original": "helloworld", "length": 10}
    assert data == expected, f"Expected JSON {expected}, but got {data}."

def test_libcruncher_so_exists():
    so_path = "/home/user/project/libcruncher.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not created."

def test_pyproject_toml_exists():
    toml_path = "/home/user/project/pyproject.toml"
    assert os.path.isfile(toml_path), f"pyproject.toml is missing at {toml_path}."
    with open(toml_path, 'r') as f:
        content = f.read()
    assert "data_org" in content or "data-org" in content, "Package name 'data_org' not found in pyproject.toml."
    assert "Flask" in content, "Flask dependency not found in pyproject.toml."
    assert "gunicorn" in content, "gunicorn dependency not found in pyproject.toml."

def test_venv_exists():
    venv_path = "/home/user/venv"
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} does not exist."
    python_bin = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable not found in {venv_path}/bin/."

def test_nginx_conf_exists():
    nginx_conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Nginx configuration file {nginx_conf_path} does not exist."

def test_nginx_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
        assert "nginx" in output, "Nginx process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check running processes.")

def test_gunicorn_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
        assert "gunicorn" in output, "Gunicorn process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check running processes.")

def test_nginx_proxy_response():
    # Test if the proxy is actually working and responding on port 8080
    url = "http://127.0.0.1:8080/api/process?data=test"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data == {"original": "test", "length": 4}, f"Unexpected response from proxy: {data}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy on port 8080: {e}")