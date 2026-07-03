# test_final_state.py

import os
import subprocess
import pytest

WORK_DIR = "/home/user/polyglot"
BUILD_SCRIPT = os.path.join(WORK_DIR, "build.sh")
LIBSEQ_C = os.path.join(WORK_DIR, "libseq.c")
VERIFY_PY = os.path.join(WORK_DIR, "verify.py")
TEST_MEM_C = os.path.join(WORK_DIR, "test_mem.c")

def setup_module(module):
    # Clean up artifacts before testing
    for f in ["build_report.txt", "libseq.so", "test_mem"]:
        path = os.path.join(WORK_DIR, f)
        if os.path.exists(path):
            os.remove(path)

def test_files_exist():
    assert os.path.isdir(WORK_DIR), f"Directory {WORK_DIR} does not exist"
    assert os.path.isfile(BUILD_SCRIPT), f"{BUILD_SCRIPT} does not exist"
    assert os.path.isfile(LIBSEQ_C), f"{LIBSEQ_C} does not exist"
    assert os.path.isfile(VERIFY_PY), f"{VERIFY_PY} does not exist"
    assert os.path.isfile(TEST_MEM_C), f"{TEST_MEM_C} does not exist"

def test_build_script_executable():
    assert os.access(BUILD_SCRIPT, os.X_OK), f"{BUILD_SCRIPT} is not executable"

def test_build_prod_mode():
    setup_module(None)
    env = os.environ.copy()
    env["BUILD_MODE"] = "PROD"

    result = subprocess.run(
        ["./build.sh"],
        cwd=WORK_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"build.sh failed in PROD mode:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    report_path = os.path.join(WORK_DIR, "build_report.txt")
    assert os.path.isfile(report_path), "build_report.txt was not created"

    with open(report_path, "r") as f:
        content = f.read().strip()
    assert content == "ALL_SYSTEMS_GO", f"build_report.txt contains incorrect text: {content}"

def test_build_debug_mode():
    setup_module(None)
    env = os.environ.copy()
    env["BUILD_MODE"] = "DEBUG"

    result = subprocess.run(
        ["./build.sh"],
        cwd=WORK_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"build.sh failed in DEBUG mode:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_verify_py_output():
    result = subprocess.run(
        ["python3", "verify.py"],
        cwd=WORK_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"verify.py failed:\n{result.stderr}"
    assert "VERIFICATION_PASSED" in result.stdout, f"verify.py did not output VERIFICATION_PASSED, got: {result.stdout}"

def test_valgrind_memory_leak():
    # Run valgrind explicitly on test_mem
    test_mem_path = os.path.join(WORK_DIR, "test_mem")
    assert os.path.isfile(test_mem_path), "test_mem executable not found"

    result = subprocess.run(
        ["valgrind", "--error-exitcode=1", "--leak-check=full", "./test_mem"],
        cwd=WORK_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Valgrind detected memory leaks:\n{result.stderr}"

def test_libseq_c_fixed():
    with open(LIBSEQ_C, "r") as f:
        content = f.read()
    assert "free(temp)" in content.replace(" ", "") or "free(temp);" in content, "libseq.c does not appear to free 'temp' to fix the memory leak."