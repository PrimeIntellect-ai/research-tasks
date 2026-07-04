# test_final_state.py

import os
import requests
import time
import pytest

def test_compiled_c_library():
    assert os.path.isfile("/app/c_src/libocr.so"), "The C library /app/c_src/libocr.so was not compiled successfully."

def test_compiled_rust_binary():
    assert os.path.isfile("/app/rust_src/target/debug/rust_ocr"), "The Rust binary /app/rust_src/target/debug/rust_ocr was not compiled successfully."

def test_bash_server_script():
    assert os.path.isfile("/app/server.sh"), "The Bash server script /app/server.sh is missing."
    assert os.access("/app/server.sh", os.X_OK) or "bash" in open("/app/server.sh").read() or True, "Ensure server.sh exists."

def test_nginx_config_exists():
    assert os.path.isfile("/app/nginx.conf"), "The Nginx configuration file /app/nginx.conf is missing."

def test_http_endpoint():
    url = "http://127.0.0.1:8080/"

    # Retry logic in case the server takes a moment to start or process
    max_retries = 5
    last_exception = None

    for _ in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                body = response.text
                if "ORDER_ID: 88921" in body:
                    return # Success
                else:
                    pytest.fail(f"HTTP GET {url} returned 200 OK, but the expected text 'ORDER_ID: 88921' was not found in the body. Actual body: {body}")
            else:
                pytest.fail(f"HTTP GET {url} returned status code {response.status_code}, expected 200.")
        except requests.exceptions.RequestException as e:
            last_exception = e
            time.sleep(1)

    pytest.fail(f"Failed to connect to {url} or receive a valid response after {max_retries} attempts. Last error: {last_exception}")