# test_final_state.py
import os
import subprocess
import pytest

LOGPROCESSOR_DIR = "/home/user/logprocessor"

def test_go_mod_exists_and_correct():
    """Verify that go.mod exists and contains the correct module name."""
    go_mod_path = os.path.join(LOGPROCESSOR_DIR, "go.mod")
    assert os.path.isfile(go_mod_path), f"Expected {go_mod_path} to exist."

    with open(go_mod_path, "r") as f:
        content = f.read()

    assert "module example.com/logprocessor" in content, "go.mod does not contain 'module example.com/logprocessor'."

def test_result_txt_correct():
    """Verify that result.txt exists and contains exactly 250."""
    result_path = os.path.join(LOGPROCESSOR_DIR, "result.txt")
    assert os.path.isfile(result_path), f"Expected {result_path} to exist."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "250", f"Expected result.txt to contain '250', but got '{content}'."

def test_mem_pprof_exists_and_valid():
    """Verify that mem.pprof exists and is a gzip compressed file."""
    pprof_path = os.path.join(LOGPROCESSOR_DIR, "mem.pprof")
    assert os.path.isfile(pprof_path), f"Expected {pprof_path} to exist."

    # Read the first two bytes to check for gzip magic number (1f 8b)
    with open(pprof_path, "rb") as f:
        magic_number = f.read(2)

    assert magic_number == b'\x1f\x8b', f"{pprof_path} does not appear to be a valid gzip compressed file (standard pprof format)."

def test_main_go_streaming_refactor():
    """Verify that main.go no longer uses ReadFile and uses os.Open instead."""
    main_go_path = os.path.join(LOGPROCESSOR_DIR, "main.go")
    assert os.path.isfile(main_go_path), f"Expected {main_go_path} to exist."

    with open(main_go_path, "r") as f:
        content = f.read()

    assert "os.ReadFile" not in content, "main.go still contains 'os.ReadFile', which reads the entire file into memory."
    assert "ioutil.ReadFile" not in content, "main.go still contains 'ioutil.ReadFile', which reads the entire file into memory."
    assert "os.Open" in content, "main.go does not contain 'os.Open'. Expected file to be opened for streaming."

def test_main_test_go_exists_and_passes():
    """Verify that main_test.go exists and `go test` passes."""
    test_go_path = os.path.join(LOGPROCESSOR_DIR, "main_test.go")
    assert os.path.isfile(test_go_path), f"Expected {test_go_path} to exist."

    # Run go test in the logprocessor directory
    result = subprocess.run(
        ["go", "test"],
        cwd=LOGPROCESSOR_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"'go test' failed with output:\n{result.stdout}\n{result.stderr}"