# test_final_state.py
import os
import subprocess
import json
import urllib.request
import urllib.error
import glob
import time
import pytest

WAF_SCRIPT = "/home/user/waf.py"
CI_CD_SCRIPT = "/home/user/ci_cd.sh"
EVIL_DIR = "/app/corpora/evil/"
CLEAN_DIR = "/app/corpora/clean/"

def test_waf_adversarial_corpus():
    """
    Test that the WAF script rejects all evil payloads and accepts all clean payloads.
    """
    assert os.path.isfile(WAF_SCRIPT), f"WAF script not found at {WAF_SCRIPT}"

    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.json"))
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.json"))

    assert len(evil_files) > 0, "No evil files found in corpus."
    assert len(clean_files) > 0, "No clean files found in corpus."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", WAF_SCRIPT, "--file", evil_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        result = subprocess.run(
            ["python3", WAF_SCRIPT, "--file", clean_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, "WAF accuracy failed:\n" + "\n".join(error_msg)

def test_nginx_config():
    """
    Test that Nginx is configured to listen on 8080 and proxy to 5000.
    """
    config_path = "/etc/nginx/sites-enabled/build_api"
    assert os.path.isfile(config_path), f"Nginx config not found at {config_path}"
    with open(config_path, "r") as f:
        content = f.read()
        assert "8080" in content, "Nginx config does not seem to listen on port 8080"
        assert "5000" in content, "Nginx config does not seem to proxy to port 5000"

def test_end_to_end_build_api():
    """
    Test the end-to-end flow by posting a clean C payload to the Nginx reverse proxy.
    """
    # Wait briefly in case services are still starting
    time.sleep(1)

    payload = {
        "source_code": "int main() { return 0; }"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "http://127.0.0.1:8080/build",
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            resp_data = json.loads(body)
            assert "checksum" in resp_data, "Response JSON missing 'checksum' key"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the build API via Nginx on port 8080: {e}")

def test_ci_cd_script_execution(tmp_path):
    """
    Test that the CI/CD script processes a directory of JSON files correctly.
    """
    assert os.path.isfile(CI_CD_SCRIPT), f"CI/CD script not found at {CI_CD_SCRIPT}"
    assert os.access(CI_CD_SCRIPT, os.X_OK), f"CI/CD script {CI_CD_SCRIPT} is not executable"

    # Create a temporary test directory with one clean and one evil payload
    test_dir = tmp_path / "test_payloads"
    test_dir.mkdir()

    clean_json = test_dir / "clean.json"
    clean_json.write_text(json.dumps({"source_code": "int main() { return 0; }"}))

    evil_json = test_dir / "evil.json"
    evil_json.write_text(json.dumps({"source_code": "int main() { system(\"ls\"); return 0; }"}))

    log_file = "/home/user/build_pipeline.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    result = subprocess.run(
        ["bash", CI_CD_SCRIPT, str(test_dir)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    assert os.path.isfile(log_file), f"Log file {log_file} was not created by the CI/CD script."

    with open(log_file, "r") as f:
        log_content = f.read()
        # The clean payload should result in a 200 OK and a checksum in the log
        assert "200" in log_content, "Expected HTTP 200 status in the log for the clean payload."
        assert "checksum" in log_content, "Expected 'checksum' in the log for the clean payload."