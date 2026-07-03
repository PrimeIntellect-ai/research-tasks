# test_final_state.py

import os

def test_process_sh_exists_and_executable():
    path = "/home/user/process.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_process_sh_no_forbidden_tools():
    path = "/home/user/process.sh"
    with open(path, "r") as f:
        content = f.read().lower()
    # Ensure forbidden tools are not used for the parsing
    for tool in ["awk", "perl", "python"]:
        assert tool not in content, f"Forbidden tool '{tool}' found in {path}."

def test_lib_rs_fixed():
    path = "/home/user/telemetry/src/lib.rs"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "#[no_mangle]" in content, f"{path} is missing #[no_mangle]."
    assert 'extern "C"' in content, f"{path} is missing extern \"C\"."

def test_rust_library_compiled():
    path = "/home/user/telemetry/target/release/libtelemetry.so"
    assert os.path.isfile(path), f"Compiled Rust library {path} does not exist."

def test_clean_csv_content():
    path = "/home/user/clean.csv"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["1,10.5", "3,15.0"]
    assert lines == expected, f"Content of {path} does not match the expected output. Got {lines}"

def test_runner_compiled():
    path = "/home/user/runner"
    assert os.path.isfile(path), f"Compiled runner binary {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_valgrind_report():
    path = "/home/user/valgrind_report.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "Memcheck" in content, f"{path} does not appear to contain Valgrind Memcheck output."