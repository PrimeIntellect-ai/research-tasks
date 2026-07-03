# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import time

def test_symlinks_exist_and_correct():
    alpha_link = "/home/user/symlinks/alpha"
    beta_link = "/home/user/symlinks/beta"

    assert os.path.islink(alpha_link), f"Symlink {alpha_link} does not exist."
    assert os.path.islink(beta_link), f"Symlink {beta_link} does not exist."

    assert os.readlink(alpha_link) == "/home/user/raw_data/proj_alpha", f"{alpha_link} points to wrong location."
    assert os.readlink(beta_link) == "/home/user/raw_data/proj_beta", f"{beta_link} points to wrong location."

def test_usage_json_exists_and_format():
    json_path = "/home/user/metrics/usage.json"
    assert os.path.isfile(json_path), f"JSON file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    assert "alpha" in data, f"'alpha' key missing in {json_path}."
    assert "beta" in data, f"'beta' key missing in {json_path}."

def test_rust_server_health_endpoint():
    url = "http://127.0.0.1:9090/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected 200 OK from {url}"
            body = response.read().decode('utf-8')
            assert '{"status": "ok"}' in body, f"Unexpected response from {url}: {body}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Rust server at {url}: {e}"

def test_rust_server_metrics_endpoint():
    url = "http://127.0.0.1:9090/metrics"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected 200 OK from {url}"
            body = response.read().decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                assert False, f"Response from {url} is not valid JSON."

            assert "alpha" in data, f"'alpha' key missing in metrics response."
            assert "beta" in data, f"'beta' key missing in metrics response."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Rust server at {url}: {e}"