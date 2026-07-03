# test_final_state.py

import os
import stat

def test_test_results_log():
    path = "/home/user/test_results.log"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the script?"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert "UNIT: OK" in content, f"{path} does not contain 'UNIT: OK'."
    assert "INTEGRATION: OK" in content, f"{path} does not contain 'INTEGRATION: OK'."

def test_proxy_conf():
    path = "/home/user/proxy.conf"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected = "upstream backend { server 127.0.0.1:8080; }"
    assert content == expected, f"{path} content is incorrect. Expected '{expected}', got '{content}'."

def test_executable_exists():
    path = "/home/user/test_router"
    assert os.path.isfile(path), f"Executable {path} is missing. Did the script compile it?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_build_script_exists_and_executable():
    path = "/home/user/build_and_test.sh"
    assert os.path.isfile(path), f"Script {path} is missing."
    assert os.access(path, os.X_OK), f"Script {path} is not executable. Did you run chmod +x?"

def test_test_router_c_exists():
    path = "/home/user/test_router.c"
    assert os.path.isfile(path), f"Source file {path} is missing."
    with open(path, 'r') as f:
        content = f.read()

    # Check if the required version strings are in the test file
    assert "1.0.0" in content, "test_router.c is missing test case for '1.0.0'"
    assert "2.1.0" in content, "test_router.c is missing test case for '2.1.0'"
    assert "2.0.9" in content, "test_router.c is missing test case for '2.0.9'"
    assert "1.9.0" in content, "test_router.c is missing test case for '1.9.0'"
    assert "1.10.0" in content, "test_router.c is missing test case for '1.10.0'"
    assert "2.0.0" in content, "test_router.c is missing test case for '2.0.0'"
    assert "1.99.9" in content, "test_router.c is missing test case for '1.99.9'"