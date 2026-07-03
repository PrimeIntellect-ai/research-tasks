# test_final_state.py

import os
import ssl
import urllib.request
import pytest

RECOVERED_DIR = "/home/user/operator/recovered"
MANIFEST_0 = os.path.join(RECOVERED_DIR, "manifest_0.yaml")
MANIFEST_1 = os.path.join(RECOVERED_DIR, "manifest_1.yaml")
SERVE_SCRIPT = "/home/user/operator/serve.py"

EXPECTED_MANIFEST_0 = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
"""

EXPECTED_MANIFEST_1 = """apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
"""

def test_recovered_directory_exists():
    assert os.path.isdir(RECOVERED_DIR), f"Directory {RECOVERED_DIR} does not exist."

def test_manifest_files_exist_and_correct():
    assert os.path.isfile(MANIFEST_0), f"File {MANIFEST_0} is missing."
    assert os.path.isfile(MANIFEST_1), f"File {MANIFEST_1} is missing."

    with open(MANIFEST_0, 'r') as f:
        content_0 = f.read()
    with open(MANIFEST_1, 'r') as f:
        content_1 = f.read()

    assert content_0.strip() == EXPECTED_MANIFEST_0.strip(), f"Content of {MANIFEST_0} does not match expected output."
    assert content_1.strip() == EXPECTED_MANIFEST_1.strip(), f"Content of {MANIFEST_1} does not match expected output."

def test_serve_script_exists():
    assert os.path.isfile(SERVE_SCRIPT), f"Script {SERVE_SCRIPT} is missing."

def test_https_server_running_and_serving_files():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8443/manifest_0.yaml"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            assert body.strip() == EXPECTED_MANIFEST_0.strip(), "HTTPS server did not return the correct content for manifest_0.yaml."
    except Exception as e:
        pytest.fail(f"Failed to fetch from HTTPS server on port 8443: {e}")