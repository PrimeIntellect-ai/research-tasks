# test_final_state.py

import os
import json
import urllib.request
import urllib.parse

def test_cmake_fixed():
    """Check if the CMake configuration was fixed to link the shared library."""
    src_cmake = "/home/user/project/src/CMakeLists.txt"
    root_cmake = "/home/user/project/CMakeLists.txt"

    fixed = False
    for path in [src_cmake, root_cmake]:
        if os.path.isfile(path):
            with open(path, "r") as f:
                content = f.read()
                if "target_link_libraries" in content and "custom_math" in content:
                    fixed = True
                    break
    assert fixed, "CMakeLists.txt was not fixed. Could not find 'target_link_libraries' linking 'custom_math'."

def test_api_and_nginx():
    """Check if Nginx is routing to the Python API and evaluating expressions correctly."""
    # Test a mathematically true expression
    url_true = "http://127.0.0.1:8080/evaluate?" + urllib.parse.urlencode({'expr': '5>3'})
    try:
        req = urllib.request.urlopen(url_true, timeout=5)
        res = req.read().decode('utf-8')
        data = json.loads(res)
        assert data.get("build") is True, f"Expected {{'build': true}} for 5>3, got {data}"
    except Exception as e:
        assert False, f"Failed to reach API via Nginx or invalid response for 5>3: {e}"

    # Test a mathematically false expression
    url_false = "http://127.0.0.1:8080/evaluate?" + urllib.parse.urlencode({'expr': '5<3'})
    try:
        req = urllib.request.urlopen(url_false, timeout=5)
        res = req.read().decode('utf-8')
        data = json.loads(res)
        assert data.get("build") is False, f"Expected {{'build': false}} for 5<3, got {data}"
    except Exception as e:
        assert False, f"Failed to reach API via Nginx or invalid response for 5<3: {e}"

def test_pipeline_output():
    """Check if the pipeline script executed correctly and produced the expected output."""
    output_file = "/home/user/pipeline_output.txt"
    assert os.path.isfile(output_file), f"Pipeline output file {output_file} is missing. Did the script run?"

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_msg = "Pipeline success. 5 * 6 = 30"
    assert expected_msg in content, f"Pipeline output does not contain the expected success message. Found: {content}"