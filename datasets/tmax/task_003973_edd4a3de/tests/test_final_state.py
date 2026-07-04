# test_final_state.py
import os
import json
import subprocess

def test_output_json():
    output_path = "/home/user/sysconf_parser/output.json"
    assert os.path.exists(output_path), f"{output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{output_path} is not valid JSON."

    expected = {
        "host": "localhost",
        "port": "8080",
        "db_path": "/var/lib/db/data.sqlite",
        "fallback_user": "admin",
        "complex_key": "some=value=with=equals",
        "missing_var": "/path"
    }

    assert data == expected, f"Output JSON content is incorrect. Expected {expected}, got {data}"

def test_requirements_txt():
    req_path = "/home/user/sysconf_parser/requirements.txt"
    assert os.path.exists(req_path), f"{req_path} does not exist."

    with open(req_path, 'r') as f:
        content = f.read().lower()

    assert "pytest" in content, "pytest not found in requirements.txt."
    assert "hypothesis" in content, "hypothesis not found in requirements.txt."

def test_test_parser_py():
    test_path = "/home/user/sysconf_parser/test_parser.py"
    assert os.path.exists(test_path), f"{test_path} does not exist."

    with open(test_path, 'r') as f:
        content = f.read()

    assert "hypothesis" in content, "hypothesis not imported in test_parser.py."

    # Run pytest on the test_parser.py file
    result = subprocess.run(["pytest", test_path], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest failed on {test_path}. Output:\n{result.stdout}\n{result.stderr}"