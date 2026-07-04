# test_final_state.py
import os
import json

def test_static_library_compiled():
    lib_path = "/home/user/polyglot-service/c_src/libapi_processor.a"
    assert os.path.isfile(lib_path), f"Static library {lib_path} was not compiled or is missing."

def test_rust_binary_compiled():
    bin_path = "/home/user/polyglot-service/target/debug/polyglot-service"
    assert os.path.isfile(bin_path), f"Rust binary {bin_path} was not compiled or is missing."

def test_results_log_content():
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"Results log {log_path} is missing."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {log_path}, found {len(lines)}."

    try:
        r1 = json.loads(lines[0])
        r2 = json.loads(lines[1])
    except json.JSONDecodeError as e:
        assert False, f"Failed to parse JSON from {log_path}: {e}"

    assert r1.get('result') == 45, f"Expected first result to be 45, got {r1.get('result')}"
    assert r2.get('result') == 42, f"Expected second result to be 42, got {r2.get('result')}"