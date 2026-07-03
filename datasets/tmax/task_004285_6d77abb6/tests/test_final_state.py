# test_final_state.py

import os
import tarfile
import subprocess
import pytest

def test_mock_request_c_exists_and_content():
    filepath = "/home/user/waf_project/tests/mock_request.c"
    assert os.path.isfile(filepath), f"File {filepath} does not exist"

    with open(filepath, "r") as f:
        content = f.read()

    assert '"POST"' in content, f"{filepath} missing 'POST' method literal"
    assert '"/login"' in content, f"{filepath} missing '/login' uri literal"
    assert '"X-Malicious"' in content, f"{filepath} missing 'X-Malicious' header_name literal"
    assert '"<script>alert(1)</script>"' in content, f"{filepath} missing XSS payload header_value literal"

def test_parser_c_patched_and_fixed():
    filepath = "/home/user/waf_project/src/parser.c"
    assert os.path.isfile(filepath), f"File {filepath} does not exist"

    with open(filepath, "r") as f:
        content = f.read()

    assert "strdup" in content and "temp_val" in content, f"{filepath} does not appear to have the patch applied"
    assert "free(" in content, f"{filepath} does not contain a call to free() to fix the memory leak"

def test_ci_pipeline_exists_and_executable():
    filepath = "/home/user/waf_project/ci_pipeline.sh"
    assert os.path.isfile(filepath), f"File {filepath} does not exist"
    assert os.access(filepath, os.X_OK), f"File {filepath} is not executable"

def test_run_tests_binary_exists_and_passes_asan():
    binary = "/home/user/waf_project/tests/run_tests"
    assert os.path.isfile(binary), f"Binary {binary} does not exist. Did the CI script compile it?"

    # Run the binary. If AddressSanitizer is enabled and a leak exists, it will exit with a non-zero code.
    env = os.environ.copy()
    env["ASAN_OPTIONS"] = "detect_leaks=1"

    try:
        result = subprocess.run([binary], env=env, capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"Binary execution failed or ASAN detected a leak. STDERR: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail(f"Binary {binary} execution timed out")

def test_deployment_tarball_exists_and_contents():
    tarpath = "/home/user/deployment.tar.gz"
    assert os.path.isfile(tarpath), f"Tarball {tarpath} does not exist"

    with tarfile.open(tarpath, "r:gz") as tar:
        names = tar.getnames()

        has_parser = any(n.endswith("src/parser.c") for n in names)
        has_waf_h = any(n.endswith("include/waf.h") for n in names)

        assert has_parser, f"src/parser.c not found in {tarpath}"
        assert has_waf_h, f"include/waf.h not found in {tarpath}"

        # Verify the packaged parser.c contains the fix
        parser_member = next(m for m in tar.getmembers() if m.name.endswith("src/parser.c"))
        f = tar.extractfile(parser_member)
        content = f.read().decode('utf-8', errors='ignore')
        assert "free(" in content, "free() not found in the packaged parser.c inside the tarball"