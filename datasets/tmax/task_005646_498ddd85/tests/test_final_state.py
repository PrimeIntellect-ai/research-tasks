# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE = "/home/user/polymath"

def test_git_repo_initialized():
    """Verify that the workspace is a Git repository."""
    git_dir = os.path.join(WORKSPACE, ".git")
    assert os.path.isdir(git_dir), "Git repository not initialized in /home/user/polymath"

def test_model_msm_content():
    """Verify the content of model.msm."""
    msm_file = os.path.join(WORKSPACE, "model.msm")
    assert os.path.isfile(msm_file), "model.msm does not exist"

    expected_content = """INPUT x y
t1 = ADD x 5.0
t2 = MUL t1 y
t3 = SUB t2 x
OUTPUT t3"""
    with open(msm_file, "r") as f:
        content = f.read().strip()

    assert content == expected_content, "model.msm content does not match expected exact content."

def test_parser_exists():
    """Verify that parser.py exists."""
    parser_file = os.path.join(WORKSPACE, "parser.py")
    assert os.path.isfile(parser_file), "parser.py does not exist"

def test_makefile_contents():
    """Verify Makefile exists and has required commands."""
    makefile = os.path.join(WORKSPACE, "Makefile")
    assert os.path.isfile(makefile), "Makefile does not exist"

    with open(makefile, "r") as f:
        content = f.read()

    assert "parser.py" in content, "Makefile does not invoke parser.py"
    assert "gcc" in content or "cc " in content, "Makefile does not compile C code using gcc/cc"
    assert "-shared" in content, "Makefile does not use -shared to build a shared library"
    assert "-fPIC" in content, "Makefile does not use -fPIC"

def test_test_model_exists():
    """Verify that test_model.py exists."""
    test_file = os.path.join(WORKSPACE, "test_model.py")
    assert os.path.isfile(test_file), "test_model.py does not exist"

def test_generated_files():
    """Verify model.c and libmodel.so are generated."""
    c_file = os.path.join(WORKSPACE, "model.c")
    so_file = os.path.join(WORKSPACE, "libmodel.so")

    assert os.path.isfile(c_file), "model.c was not generated"
    assert os.path.isfile(so_file), "libmodel.so was not generated"

def test_result_txt():
    """Verify result.txt contains the correct computed value."""
    result_file = os.path.join(WORKSPACE, "result.txt")
    assert os.path.isfile(result_file), "result.txt does not exist"

    with open(result_file, "r") as f:
        res = f.read().strip()

    try:
        val = float(res)
    except ValueError:
        pytest.fail(f"result.txt content '{res}' is not a valid float")

    assert val == 29.0, f"Expected result.txt to contain 29.0, but got {val}"

def test_pre_commit_hook():
    """Verify pre-commit hook exists, is executable, and contains required commands."""
    hook_file = os.path.join(WORKSPACE, ".git", "hooks", "pre-commit")
    assert os.path.isfile(hook_file), "pre-commit hook does not exist"

    assert os.access(hook_file, os.X_OK), "pre-commit hook is not executable"

    with open(hook_file, "r") as f:
        content = f.read()

    assert "make" in content, "pre-commit hook does not run 'make'"
    assert "test_model.py" in content, "pre-commit hook does not run test_model.py"