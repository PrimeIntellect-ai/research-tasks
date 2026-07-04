# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_success_log_exists_and_correct():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"Expected file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "patch_7.diff", f"Expected success.log to contain 'patch_7.diff', but found '{content}'"

def test_emulator_exists():
    emulator_path = "/home/user/emulator.py"
    assert os.path.isfile(emulator_path), f"Expected emulator script at {emulator_path} does not exist."

def run_emulator(dsl_content: str) -> int:
    emulator_path = "/home/user/emulator.py"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lt', delete=False) as tmp:
        tmp.write(dsl_content)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["python3", emulator_path, tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.returncode
    finally:
        os.remove(tmp_path)

def test_emulator_valid_input():
    valid_dsl = """
    # This is a comment
    ALLOC A
    ALLOC B
    USE A
    USE B
    FREE A
    FREE B
    """
    exit_code = run_emulator(valid_dsl)
    assert exit_code == 0, "Emulator failed (non-zero exit code) on valid DSL input."

def test_emulator_double_alloc():
    dsl = """
    ALLOC X
    ALLOC X
    """
    exit_code = run_emulator(dsl)
    assert exit_code == 1, "Emulator did not exit with code 1 on Double Alloc."

def test_emulator_double_free():
    dsl = """
    ALLOC X
    FREE X
    FREE X
    """
    exit_code = run_emulator(dsl)
    assert exit_code == 1, "Emulator did not exit with code 1 on Double Free."

def test_emulator_uninitialized_free():
    dsl = """
    FREE Y
    """
    exit_code = run_emulator(dsl)
    assert exit_code == 1, "Emulator did not exit with code 1 on Uninitialized Free."

def test_emulator_use_after_free():
    dsl = """
    ALLOC Z
    FREE Z
    USE Z
    """
    exit_code = run_emulator(dsl)
    assert exit_code == 1, "Emulator did not exit with code 1 on Use After Free."

def test_emulator_uninitialized_use():
    dsl = """
    USE W
    """
    exit_code = run_emulator(dsl)
    assert exit_code == 1, "Emulator did not exit with code 1 on Uninitialized Use."