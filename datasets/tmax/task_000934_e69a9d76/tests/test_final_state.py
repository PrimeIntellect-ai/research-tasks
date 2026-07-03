# test_final_state.py
import os
import json
import subprocess
import time
import pytest
import requests

def test_loc_server_binary_exists():
    assert os.path.exists("/home/user/loc_server"), "/home/user/loc_server does not exist"
    assert os.access("/home/user/loc_server", os.X_OK), "/home/user/loc_server is not executable"

def test_flush_pipeline_script_exists():
    assert os.path.exists("/home/user/flush_pipeline.sh"), "/home/user/flush_pipeline.sh does not exist"
    assert os.access("/home/user/flush_pipeline.sh", os.X_OK), "/home/user/flush_pipeline.sh is not executable"

def test_crontab_entry_exists():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to list crontab"
    assert "/home/user/flush_pipeline.sh" in result.stdout, "Crontab does not contain /home/user/flush_pipeline.sh"

def test_http_service_translations_and_stats():
    base_url = "http://127.0.0.1:8080"

    # Wait for the service to be up if needed, though it should be running in the background.
    try:
        requests.get(f"{base_url}/stats", timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("HTTP server is not running on 127.0.0.1:8080")

    # Send first batch
    payload1 = [
        {"lang": "de", "orig": "Welcome", "trans": "Willkommen"}, # diff 3 -> 0.70
        {"lang": "de", "orig": "Cat", "trans": "Katze"}           # diff 2 -> 0.80
    ]
    resp = requests.post(f"{base_url}/translations", json=payload1, timeout=5)
    assert resp.status_code in (200, 201, 202, 204), f"POST /translations failed: {resp.status_code}"

    # Check stats
    resp = requests.get(f"{base_url}/stats", timeout=5)
    assert resp.status_code == 200, f"GET /stats failed: {resp.status_code}"
    stats = resp.json()
    assert "de" in stats, "Language 'de' not found in stats"
    assert abs(stats["de"] - 0.75) < 0.01, f"Expected 'de' average to be ~0.75, got {stats['de']}"

    # Send low quality batch
    payload2 = [
        {"lang": "es", "orig": "Very long string here", "trans": "Short"} # diff 16 -> 0.10
    ]
    resp = requests.post(f"{base_url}/translations", json=payload2, timeout=5)
    assert resp.status_code in (200, 201, 202, 204), f"POST /translations failed: {resp.status_code}"

    # Check stats again
    resp = requests.get(f"{base_url}/stats", timeout=5)
    assert resp.status_code == 200, f"GET /stats failed: {resp.status_code}"
    stats = resp.json()
    assert "es" in stats, "Language 'es' not found in stats"
    assert abs(stats["es"] - 0.10) < 0.01, f"Expected 'es' average to be ~0.10, got {stats['es']}"

def test_low_quality_samples_file():
    samples_file = "/home/user/low_quality_samples.json"
    assert os.path.exists(samples_file), f"File {samples_file} does not exist"

    with open(samples_file, "r", encoding="utf-8") as f:
        try:
            samples = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {samples_file} does not contain valid JSON")

    assert isinstance(samples, list), f"Expected JSON array in {samples_file}"
    es_samples = [s for s in samples if s.get("lang") == "es"]
    assert len(es_samples) >= 1, "Expected at least one 'es' sample in low_quality_samples.json"
    assert es_samples[-1].get("orig") == "Very long string here", "Sample original text does not match"

def test_flush_endpoint():
    base_url = "http://127.0.0.1:8080"
    resp = requests.post(f"{base_url}/flush", timeout=5)
    assert resp.status_code in (200, 201, 202, 204), f"POST /flush failed: {resp.status_code}"

    resp = requests.get(f"{base_url}/stats", timeout=5)
    assert resp.status_code == 200, f"GET /stats failed: {resp.status_code}"
    stats = resp.json()
    assert len(stats) == 0 or all(v == 0.0 for v in stats.values()), "Stats were not cleared after /flush"