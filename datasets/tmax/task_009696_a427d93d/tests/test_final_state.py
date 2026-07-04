# test_final_state.py

import os
import json
import re
import subprocess
import pytest

def test_process_artifacts_script_exists():
    script_path = '/home/user/process_artifacts.py'
    assert os.path.isfile(script_path), f"{script_path} is missing"

def test_extractor_compiled_and_executable():
    extractor_path = '/home/user/build_tools/extractor'
    assert os.path.isfile(extractor_path), f"{extractor_path} binary is missing. Did you run make?"
    assert os.access(extractor_path, os.X_OK), f"{extractor_path} binary is not executable"

def test_extractor_execution_fixed():
    extractor_path = '/home/user/build_tools/extractor'
    if not os.path.isfile(extractor_path):
        pytest.skip("extractor binary not found")

    test_file = '/tmp/test_artifact_long.bin'
    # 60 characters long hex string to test buffer overflow fix (original buffer was 16)
    test_hex = "41" * 60
    with open(test_file, 'w') as f:
        f.write(f"JUNK_HEX[{test_hex}]JUNK")

    result = subprocess.run([extractor_path, test_file], capture_output=True, text=True)
    assert result.returncode == 0, "extractor crashed or returned non-zero exit code when processing long hex data. Memory safety issue might still exist."
    assert f"ENCODED:{test_hex}" in result.stdout, "extractor did not output the correct ENCODED string for long hex data. Buffer overflow or truncation might still exist."

def test_artifact_metrics_json_correct():
    json_path = '/home/user/artifact_metrics.json'
    assert os.path.isfile(json_path), f"{json_path} is missing"

    with open(json_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON")

    artifacts_dir = '/home/user/artifacts'
    expected_metrics = {}

    for filename in os.listdir(artifacts_dir):
        if filename.endswith('.bin'):
            file_path = os.path.join(artifacts_dir, filename)
            with open(file_path, 'r') as f:
                content = f.read()

            match = re.search(r'HEX\[(.*?)\]', content)
            assert match is not None, f"Could not find HEX marker in {filename}"
            hex_data = match.group(1)

            decoded = bytes.fromhex(hex_data).decode('ascii')
            result = eval(decoded)
            expected_metrics[filename] = int(result)

    assert metrics == expected_metrics, "The /home/user/artifact_metrics.json does not match the expected evaluated metrics."