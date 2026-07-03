# test_final_state.py
import os
import subprocess
import pytest

def test_version_tests_log():
    log_path = "/home/user/version_tests.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    # Filter out empty lines just in case
    content = [line.strip() for line in content if line.strip()]

    expected = [
        "[CROSS COMPILE MODE ENABLED]",
        "1",
        "[CROSS COMPILE MODE ENABLED]",
        "0",
        "[CROSS COMPILE MODE ENABLED]",
        "-1"
    ]

    assert content == expected, f"Contents of {log_path} do not match the expected output. Got: {content}"

def test_benchmark_results_log():
    log_path = "/home/user/benchmark_results.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "Benchmark completed: 5000 requests processed." in content, f"{log_path} does not contain the expected benchmark completion message."

def test_makefile_cross_compile_mode():
    makefile_path = "/home/user/build_router/Makefile"
    assert os.path.isfile(makefile_path), f"File {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "CROSS_COMPILE_MODE" in content, "Makefile does not contain 'CROSS_COMPILE_MODE' as required for the ARCH=cross conditional."

def test_url_parser_segfault_fixed():
    router_path = "/home/user/build_router/router"
    assert os.path.isfile(router_path), f"Executable {router_path} is missing. Did you compile the project?"
    assert os.access(router_path, os.X_OK), f"{router_path} is not executable."

    try:
        result = subprocess.run(
            [router_path, "parse", "build://project/1.2.3"],
            capture_output=True,
            text=True,
            timeout=2
        )
        assert result.returncode == 0, f"Router exited with code {result.returncode} when parsing a URL without '?arch='. It might still be segfaulting."
        assert "ARCH: NONE" in result.stdout, "Router did not print 'ARCH: NONE' for a URL missing the architecture parameter."
    except subprocess.TimeoutExpired:
        pytest.fail("Router timed out when parsing a URL without '?arch='.")