# test_final_state.py
import os
import subprocess
import pytest

def test_tinyexpr_makefile_fixed():
    makefile_path = '/app/tinyexpr/Makefile'
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing"

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert '-ffast-math' not in content, "Makefile still contains the '-ffast-math' flag"

def test_tinyexpr_make_test_passes():
    try:
        result = subprocess.run(['make', 'test'], cwd='/app/tinyexpr', capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"`make test` failed with exit code {result.returncode}.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("`make test` timed out")

def test_recovered_directories():
    clean_dir = '/home/user/clean'
    evil_dir = '/home/user/evil'

    assert os.path.isdir(clean_dir), f"{clean_dir} directory is missing"
    assert os.path.isdir(evil_dir), f"{evil_dir} directory is missing"

    clean_files = os.listdir(clean_dir)
    evil_files = os.listdir(evil_dir)

    assert len(clean_files) > 0, f"No recovered files found in {clean_dir}"
    assert len(evil_files) > 0, f"No recovered files found in {evil_dir}"

def test_filter_expr_executable():
    script_path = '/home/user/filter_expr'
    assert os.path.isfile(script_path), f"{script_path} is missing"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

def test_adversarial_corpus():
    script_path = '/home/user/filter_expr'
    clean_dir = '/verify/clean'
    evil_dir = '/verify/evil'

    assert os.path.isdir(clean_dir), f"Verifier clean corpus directory {clean_dir} is missing"
    assert os.path.isdir(evil_dir), f"Verifier evil corpus directory {evil_dir} is missing"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_modified = []
    evil_bypassed = []

    for cf in clean_files:
        filepath = os.path.join(clean_dir, cf)
        result = subprocess.run([script_path, filepath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(cf)

    for ef in evil_files:
        filepath = os.path.join(evil_dir, ef)
        result = subprocess.run([script_path, filepath], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(ef)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))