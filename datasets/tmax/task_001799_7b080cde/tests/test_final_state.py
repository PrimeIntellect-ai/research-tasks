# test_final_state.py

import os
import requests
import pytest

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "[SUCCESS] Processed fr - 2 keys loaded." in content, "Missing or incorrect log entry for 'fr' in pipeline.log."
    assert "[SUCCESS] Processed ja - 2 keys loaded." in content, "Missing or incorrect log entry for 'ja' in pipeline.log."

def test_translation_api_ja():
    url = "http://127.0.0.1:9000/translate/ja/GREETING"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Rust service at {url}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for {url}, got {resp.status_code}"
    assert resp.text == "こんにちは", f"Expected 'こんにちは', got '{resp.text}'"

    url_farewell = "http://127.0.0.1:9000/translate/ja/FAREWELL"
    resp = requests.get(url_farewell, timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK for {url_farewell}, got {resp.status_code}"
    assert resp.text == "さようなら", f"Expected 'さようなら', got '{resp.text}'"

def test_translation_api_fr():
    url = "http://127.0.0.1:9000/translate/fr/WELCOME"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Rust service at {url}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for {url}, got {resp.status_code}"
    assert resp.text == "Bienvenue", f"Expected 'Bienvenue', got '{resp.text}'"

    url_farewell = "http://127.0.0.1:9000/translate/fr/FAREWELL"
    resp = requests.get(url_farewell, timeout=5)
    assert resp.status_code == 200, f"Expected 200 OK for {url_farewell}, got {resp.status_code}"
    assert resp.text == "Au revoir", f"Expected 'Au revoir', got '{resp.text}'"

def test_translation_api_not_found():
    url = "http://127.0.0.1:9000/translate/fr/UNKNOWN_KEY"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Rust service at {url}: {e}")

    assert resp.status_code == 404, f"Expected 404 Not Found for {url}, got {resp.status_code}"