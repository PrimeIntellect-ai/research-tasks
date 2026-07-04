# test_final_state.py
import os
import urllib.request
import pytest

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def test_nginx_config_updated():
    config_path = "/home/user/nginx.conf"
    assert os.path.exists(config_path), f"Nginx config missing at {config_path}"
    with open(config_path, 'r') as f:
        content = f.read()
        assert "unix:/tmp/dtmf.sock" in content, "Nginx config not updated to point to /tmp/dtmf.sock"

def test_dtmf_decoding_api():
    expected = "8675309"
    try:
        response = urllib.request.urlopen('http://127.0.0.1:8080/decode', timeout=5)
        result = response.read().decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to connect to or read from http://127.0.0.1:8080/decode: {e}")

    result_clean = ''.join(filter(str.isalnum, result))
    distance = levenshtein_distance(result_clean, expected)
    cer = distance / len(expected)

    assert cer <= 0.2, f"CER {cer:.3f} exceeds threshold 0.2. Expected: '{expected}', Got: '{result_clean}'"