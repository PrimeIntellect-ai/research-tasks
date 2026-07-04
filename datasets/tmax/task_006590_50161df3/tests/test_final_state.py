# test_final_state.py

import os
import stat
import subprocess
import tempfile
import shutil
import pytest

def test_cycle_log_content():
    """Check if cycle.log contains the correct cycle."""
    log_path = '/home/user/project/cycle.log'
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_cycle = "Cycle: Core -> Utils -> Network -> Core"
    assert expected_cycle in content, f"Expected '{expected_cycle}' in {log_path}, got: {content}"

def test_build_deps_fixed():
    """Check if build.deps is fixed by removing the Utils -> Network dependency."""
    deps_path = '/home/user/project/build.deps'
    assert os.path.isfile(deps_path), f"{deps_path} is missing."

    with open(deps_path, 'r') as f:
        content = f.read()

    # Check that Utils -> Network is no longer present
    # It could be 'Utils ->' or 'Utils -> SomethingElse' but 'Network' should not be in Utils' list.
    for line in content.splitlines():
        if line.strip().startswith('Utils'):
            # If there's an arrow, check if Network is in the right side
            if '->' in line:
                deps = line.split('->')[1]
                assert 'Network' not in deps, f"Circular dependency 'Network' still found in Utils dependencies: {line}"

def test_cpp_file_exists():
    """Check if cycle_detector.cpp exists."""
    cpp_path = '/home/user/project/cycle_detector.cpp'
    assert os.path.isfile(cpp_path), f"{cpp_path} is missing."

def test_ci_pipeline_exists_and_executable():
    """Check if ci_pipeline.sh exists and is executable."""
    script_path = '/home/user/project/ci_pipeline.sh'
    assert os.path.isfile(script_path), f"{script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_ci_pipeline_execution():
    """Run ci_pipeline.sh with fixed build.deps and verify it passes, then test with broken build.deps."""
    script_path = '/home/user/project/ci_pipeline.sh'
    deps_path = '/home/user/project/build.deps'

    # Run with current (fixed) build.deps
    result_fixed = subprocess.run([script_path], cwd='/home/user/project', capture_output=True)
    assert result_fixed.returncode == 0, f"{script_path} failed on fixed build.deps. Output: {result_fixed.stderr.decode()}"

    # Create a broken build.deps to test the pipeline
    broken_deps = """Core -> Utils, Math
Math -> Utils
Network -> Core, Crypto
Crypto -> Utils
App -> Network, UI
UI -> Core
Utils -> Network
"""
    # Backup fixed build.deps
    backup_path = '/home/user/project/build.deps.bak'
    shutil.copy(deps_path, backup_path)

    try:
        with open(deps_path, 'w') as f:
            f.write(broken_deps)

        # Run with broken build.deps
        result_broken = subprocess.run([script_path], cwd='/home/user/project', capture_output=True)
        assert result_broken.returncode == 1, f"{script_path} should have exited with 1 on broken build.deps, got {result_broken.returncode}."
    finally:
        # Restore fixed build.deps
        shutil.move(backup_path, deps_path)