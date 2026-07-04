# test_final_state.py

import os
import json
import subprocess

def test_data_json_unmodified():
    data_path = '/home/user/build_debug/data.json'
    assert os.path.isfile(data_path), f"{data_path} is missing"

    # Check that it's encoded in utf-16le and contains the right data
    try:
        with open(data_path, 'r', encoding='utf-16le') as f:
            data = json.load(f)
        assert data == {'values': [0.1, 0.2]}, "data.json was modified or corrupted"
    except Exception as e:
        assert False, f"Failed to read data.json with utf-16le encoding. Was it modified? Error: {e}"

def test_pytest_passes():
    test_path = '/home/user/build_debug/test_processor.py'
    assert os.path.isfile(test_path), f"{test_path} is missing"

    # Run pytest on the test_processor.py
    result = subprocess.run(
        ['python3', '-m', 'pytest', test_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"pytest failed with exit code {result.returncode}.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"

def test_processor_py_fixed():
    processor_path = '/home/user/build_debug/processor.py'
    assert os.path.isfile(processor_path), f"{processor_path} is missing"

    with open(processor_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The file should now handle the encoding
    assert "utf-16" in content.lower(), "processor.py does not appear to fix the utf-16 encoding issue"

def test_test_processor_py_fixed():
    test_path = '/home/user/build_debug/test_processor.py'
    assert os.path.isfile(test_path), f"{test_path} is missing"

    with open(test_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The file should no longer have the strict equality bug
    assert "assert result == 0.3" not in content, "test_processor.py still contains the exact 'assert result == 0.3' bug"