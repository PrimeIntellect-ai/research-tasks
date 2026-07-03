# test_final_state.py

import os
import json
import configparser

def test_config_updated():
    config_path = "/home/user/pipeline/config.ini"
    assert os.path.isfile(config_path), f"File missing: {config_path}"

    config = configparser.ConfigParser()
    config.read(config_path)

    assert 'Settings' in config, "[Settings] section missing in config.ini"
    assert 'chunk_size' in config['Settings'], "chunk_size missing in config.ini"
    assert config['Settings']['chunk_size'] == '10000', "chunk_size was not updated to 10000"

def test_result_json_correct():
    result_path = "/home/user/pipeline/result.json"
    assert os.path.isfile(result_path), f"File missing: {result_path}"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "result.json is not valid JSON"

    assert "naive_sum" in data, "naive_sum missing in result.json"
    assert "precise_sum" in data, "precise_sum missing in result.json"
    assert "corrupted_count" in data, "corrupted_count missing in result.json"

    assert data["naive_sum"] == 10000000000001000.0, f"naive_sum incorrect: expected 10000000000001000.0, got {data['naive_sum']}"
    assert data["precise_sum"] == 10000000000002000.0, f"precise_sum incorrect: expected 10000000000002000.0, got {data['precise_sum']}"
    assert data["corrupted_count"] == 50, f"corrupted_count incorrect: expected 50, got {data['corrupted_count']}"

def test_regression_test_file():
    test_path = "/home/user/pipeline/test_precision.py"
    assert os.path.isfile(test_path), f"Regression test file missing: {test_path}"

    with open(test_path, 'r') as f:
        content = f.read()

    assert "test_precision_recovery" in content, "Function 'test_precision_recovery' missing in test_precision.py"
    assert "1e16" in content, "The value '1e16' is missing in test_precision.py"
    assert "math.fsum" in content or "fsum" in content, "math.fsum usage missing in test_precision.py"