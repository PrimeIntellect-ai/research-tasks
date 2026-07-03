# test_final_state.py
import os
import urllib.request
import urllib.error
import pytest
import subprocess
import time

def test_nginx_config_updated():
    conf_path = "/home/user/iot_pipeline/nginx/nginx.conf"
    assert os.path.exists(conf_path), f"Missing {conf_path}"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "8081" in content, "nginx.conf was not updated to point to port 8081"
    assert "9000" not in content, "nginx.conf still contains the old port 9000"

def test_makefile_updated():
    makefile_path = "/home/user/iot_pipeline/src/Makefile"
    assert os.path.exists(makefile_path), f"Missing {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-rpath" in content or "-R" in content or "RPATH" in content.upper(), "Makefile does not contain RPATH configuration"

def test_adversarial_corpus():
    # Attempt to start services to ensure they are running
    subprocess.run(["bash", "start_services.sh"], cwd="/home/user/iot_pipeline", capture_output=True)
    time.sleep(2)

    clean_dir = "/home/user/corpora/clean/"
    evil_dir = "/home/user/corpora/evil/"

    assert os.path.exists(clean_dir), f"Missing clean corpus dir: {clean_dir}"
    assert os.path.exists(evil_dir), f"Missing evil corpus dir: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "Clean corpus is empty"
    assert len(evil_files) > 0, "Evil corpus is empty"

    clean_modified = []
    evil_bypassed = []

    for cf in clean_files:
        with open(cf, "rb") as f:
            data = f.read()
        req = urllib.request.Request("http://localhost:8080/ingest", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status != 200:
                    clean_modified.append(os.path.basename(cf))
        except urllib.error.URLError:
            clean_modified.append(os.path.basename(cf))

    for ef in evil_files:
        with open(ef, "rb") as f:
            data = f.read()
        req = urllib.request.Request("http://localhost:8080/ingest", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    evil_bypassed.append(os.path.basename(ef))
        except urllib.error.URLError:
            # Rejection via 400 or connection close is expected
            pass

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))