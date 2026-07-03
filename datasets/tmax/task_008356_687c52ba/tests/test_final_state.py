# test_final_state.py

import os
import re
import subprocess
import pytest

def test_cmakelists_linked():
    cmakelists_path = '/home/user/project/CMakeLists.txt'
    assert os.path.isfile(cmakelists_path), f"{cmakelists_path} is missing"
    with open(cmakelists_path, 'r') as f:
        content = f.read()

    # Check if target_link_libraries links test_encoder and protorest
    assert re.search(r'target_link_libraries\s*\(\s*test_encoder\s+protorest\s*\)', content, re.IGNORECASE), \
        "CMakeLists.txt is missing target_link_libraries(test_encoder protorest)"

def test_test_encoder_c_contains_test():
    test_c_path = '/home/user/project/tests/test_encoder.c'
    assert os.path.isfile(test_c_path), f"{test_c_path} is missing"
    with open(test_c_path, 'r') as f:
        content = f.read()

    assert "test_rest_payload" in content, "test_rest_payload function is missing in test_encoder.c"
    assert '"Migrating to Py3"' in content, "test_rest_payload does not contain the correct input string"
    assert '{"payload": "TWlncmF0aW5nIHRvIFB5Mw=="}' in content, "test_rest_payload does not contain the correct expected JSON string"

    # Check if it's called in main
    main_match = re.search(r'int\s+main\s*\([^)]*\)\s*\{([^}]+)\}', content)
    assert main_match is not None, "main function not found in test_encoder.c"
    assert "test_rest_payload" in main_match.group(1), "test_rest_payload is not called in main()"

def test_build_success():
    build_dir = '/home/user/project/build'
    assert os.path.isdir(build_dir), f"Build directory {build_dir} is missing"

    # Run cmake and make to verify it builds successfully
    cmake_res = subprocess.run(['cmake', '..'], cwd=build_dir, capture_output=True, text=True)
    assert cmake_res.returncode == 0, f"CMake configuration failed:\n{cmake_res.stderr}"

    make_res = subprocess.run(['make'], cwd=build_dir, capture_output=True, text=True)
    assert make_res.returncode == 0, f"Make build failed (possibly linker error):\n{make_res.stderr}"

    executable_path = os.path.join(build_dir, 'test_encoder')
    assert os.path.isfile(executable_path), f"Executable {executable_path} was not built"

def test_executable_runs_successfully():
    executable_path = '/home/user/project/build/test_encoder'
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing"

    run_res = subprocess.run([executable_path], capture_output=True, text=True)
    assert run_res.returncode == 0, f"Test executable failed to run, possibly due to assertion failure:\n{run_res.stderr}"

def test_test_result_log():
    log_path = '/home/user/test_result.log'
    assert os.path.isfile(log_path), f"{log_path} is missing"
    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "SUCCESS", f"Expected 'SUCCESS' in {log_path}, but got '{content}'"