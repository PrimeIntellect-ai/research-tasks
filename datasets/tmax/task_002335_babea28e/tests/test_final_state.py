# test_final_state.py

import os
import re
import stat
import pytest

WORKSPACE_DIR = "/home/user/workspace"
AUTH_MODULE_DIR = os.path.join(WORKSPACE_DIR, "auth_module")
CI_RUN_SH = os.path.join(AUTH_MODULE_DIR, "ci_run.sh")
CI_RESULT_LOG = os.path.join(WORKSPACE_DIR, "ci_result.log")
CMAKE_LISTS = os.path.join(AUTH_MODULE_DIR, "CMakeLists.txt")
AUTH_TEST_CPP = os.path.join(AUTH_MODULE_DIR, "auth_test.cpp")

def test_ci_run_script_exists_and_executable():
    assert os.path.isfile(CI_RUN_SH), f"CI script not found at {CI_RUN_SH}"
    st = os.stat(CI_RUN_SH)
    assert bool(st.st_mode & stat.S_IXUSR), f"CI script at {CI_RUN_SH} is not executable"

def test_ci_result_log_exists():
    assert os.path.isfile(CI_RESULT_LOG), f"Result log not found at {CI_RESULT_LOG}"

def test_ci_result_log_content():
    with open(CI_RESULT_LOG, 'r') as f:
        content = f.read()

    assert "All tests passed!" in content, "Log does not contain 'All tests passed!'"

    asan_keywords = ["AddressSanitizer", "leak", "ERROR: LeakSanitizer"]
    for kw in asan_keywords:
        assert kw not in content, f"Log contains ASan error/warning keyword: {kw}"

def test_cmake_lists_fixed():
    assert os.path.isfile(CMAKE_LISTS), f"CMakeLists.txt not found at {CMAKE_LISTS}"
    with open(CMAKE_LISTS, 'r') as f:
        content = f.read()

    assert "target_link_libraries" in content, "CMakeLists.txt is missing target_link_libraries"
    assert "RPATH" in content or "rpath" in content.lower(), "CMakeLists.txt is missing RPATH configuration"
    assert "mock_waf" in content or "libmock_waf.so" in content, "CMakeLists.txt does not link against mock_waf"

def test_auth_test_cpp_fixed():
    assert os.path.isfile(AUTH_TEST_CPP), f"auth_test.cpp not found at {AUTH_TEST_CPP}"
    with open(AUTH_TEST_CPP, 'r') as f:
        content = f.read()

    # Check for memory leak fix
    malformed_block = re.search(r'if\s*\(\s*token\s*==\s*"malformed"\s*\)\s*\{([^}]+)\}', content)
    assert malformed_block is not None, "Could not find 'malformed' if-block in auth_test.cpp"
    assert "delete[]" in malformed_block.group(1), "Memory leak not fixed: missing 'delete[] buffer;' in 'malformed' token branch"

    # Check for constraint satisfaction implementation
    assert 'return "";' not in content, "generate_attack_payload is still returning an empty string"