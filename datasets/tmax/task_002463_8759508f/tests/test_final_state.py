# test_final_state.py
import os
import subprocess
import urllib.request
import pytest

def test_redis_metadata():
    """Check that Redis contains the correct metadata for alpha and beta."""
    # Check alpha
    cmd_alpha = ["redis-cli", "get", "meta:author:alpha"]
    res_alpha = subprocess.run(cmd_alpha, capture_output=True, text=True)
    assert res_alpha.returncode == 0, "Failed to run redis-cli"
    alpha_val = res_alpha.stdout.strip()
    assert alpha_val == "Dr. Turing", f"Incorrect Redis alpha metadata. Expected 'Dr. Turing', got '{alpha_val}'"

    # Check beta
    cmd_beta = ["redis-cli", "get", "meta:author:beta"]
    res_beta = subprocess.run(cmd_beta, capture_output=True, text=True)
    assert res_beta.returncode == 0, "Failed to run redis-cli"
    beta_val = res_beta.stdout.strip()
    assert beta_val == "Dr. Lovelace", f"Incorrect Redis beta metadata. Expected 'Dr. Lovelace', got '{beta_val}'"

def test_artifacts_size():
    """Check that the total size of the artifacts directory is under the threshold."""
    artifacts_dir = "/home/user/artifacts"
    assert os.path.exists(artifacts_dir), f"Directory {artifacts_dir} does not exist"

    size_cmd = subprocess.run(['du', '-sb', artifacts_dir], capture_output=True, text=True)
    assert size_cmd.returncode == 0, "Failed to run du command"

    total_size = int(size_cmd.stdout.split()[0])
    threshold = 850000

    assert total_size <= threshold, f"Artifacts too large: {total_size} bytes > {threshold} bytes. Did you convert hex to binary before compressing?"
    assert total_size > 4096, f"Artifacts directory size ({total_size} bytes) is suspiciously small, likely empty."

def test_nginx_serving():
    """Check that Nginx is serving the generated artifacts correctly."""
    artifacts_dir = "/home/user/artifacts"
    assert os.path.exists(artifacts_dir), f"Directory {artifacts_dir} does not exist"

    files = [f for f in os.listdir(artifacts_dir) if os.path.isfile(os.path.join(artifacts_dir, f))]
    assert len(files) > 0, "No files found in artifacts directory to serve"

    for f in files:
        url = f"http://127.0.0.1:8080/{f}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"Failed to fetch {f} from Nginx (status {response.status})"
                content = response.read()
                assert len(content) > 0, f"File {f} served by Nginx is empty"
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to fetch {f} from Nginx at {url}: {e}")