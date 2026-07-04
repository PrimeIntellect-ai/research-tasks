# test_final_state.py

import os
import re
import time
import subprocess
import py_compile

def test_protobuf_compiled():
    pb2_file = "/home/user/request_pb2.py"
    assert os.path.isfile(pb2_file), f"Protobuf bindings not found at {pb2_file}"

def test_legacy_parser_python3():
    parser_file = "/home/user/legacy_parser.py"
    assert os.path.isfile(parser_file), f"File {parser_file} is missing."

    # Check syntax validity for Python 3
    try:
        py_compile.compile(parser_file, doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"{parser_file} is not valid Python 3: {e}")

    with open(parser_file, "r") as f:
        content = f.read()

    assert "urllib.parse" in content, f"Expected 'urllib.parse' in {parser_file} for Python 3 compatibility."
    assert "sys.stdout.buffer.write" in content or "sys.stdout.write" in content, \
        f"Expected stdout write method in {parser_file}."
    assert "urlparse" not in content.split(), f"Found Python 2 'urlparse' in {parser_file}."

def test_process_requests_executable():
    script_file = "/home/user/process_requests.sh"
    assert os.path.isfile(script_file), f"Script {script_file} is missing."
    assert os.access(script_file, os.X_OK), f"Script {script_file} is not executable."

def test_processing_log_content():
    log_file = "/home/user/processing.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_patterns = [
        r"^Domain: api\.example\.com \| URL: https://api\.example\.com/v1/users \| PeakMem: \d+ KB$",
        r"^Domain: legacy\.internal\.net \| URL: http://legacy\.internal\.net/status \| PeakMem: \d+ KB$",
        r"^Domain: grpc\.service\.org \| URL: https://grpc\.service\.org/v2/update \| PeakMem: \d+ KB$"
    ]

    # The log file might have more lines if the script was run multiple times, 
    # but it should contain at least one set of these 3 lines.
    # We will check if all expected patterns are found in the log.
    for pattern in expected_patterns:
        found = any(re.match(pattern, line) for line in lines)
        assert found, f"Could not find a line matching pattern '{pattern}' in {log_file}."

def test_script_execution_time():
    script_file = "/home/user/process_requests.sh"
    assert os.path.isfile(script_file), f"Script {script_file} is missing."

    start_time = time.time()
    result = subprocess.run([script_file], capture_output=True, text=True)
    end_time = time.time()

    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    elapsed = end_time - start_time
    assert elapsed >= 3.0, f"Script execution time was {elapsed:.2f}s, expected at least 3.0s due to rate limiting."