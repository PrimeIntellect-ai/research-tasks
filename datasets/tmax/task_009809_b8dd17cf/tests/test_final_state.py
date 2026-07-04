# test_final_state.py

import os
import subprocess
import json
import pytest

PROJECT_DIR = '/home/user/project'

def test_wrapper_is_valid_python3():
    wrapper_path = os.path.join(PROJECT_DIR, 'wrapper.py')
    assert os.path.isfile(wrapper_path), f"{wrapper_path} does not exist"

    # Check if it compiles as Python 3
    result = subprocess.run(['python3', '-m', 'py_compile', wrapper_path], capture_output=True)
    assert result.returncode == 0, f"wrapper.py is not valid Python 3. Error:\n{result.stderr.decode()}"

    # Check that Python 2 constructs are gone
    with open(wrapper_path, 'r') as f:
        content = f.read()
    assert 'print ' not in content, "Python 2 print statement still exists in wrapper.py"
    assert '.iteritems()' not in content, "Python 2 iteritems() still exists in wrapper.py"

def test_test_semver_cpp_exists_and_includes_rapidcheck():
    test_file = os.path.join(PROJECT_DIR, 'test_semver.cpp')
    assert os.path.isfile(test_file), f"{test_file} does not exist"

    with open(test_file, 'r') as f:
        content = f.read()
    assert '<rapidcheck.h>' in content, "test_semver.cpp does not include <rapidcheck.h>"

def test_ci_sh_exists_and_executable():
    ci_script = os.path.join(PROJECT_DIR, 'ci.sh')
    assert os.path.isfile(ci_script), f"{ci_script} does not exist"
    assert os.access(ci_script, os.X_OK), f"{ci_script} is not executable"

def test_ci_sh_execution_and_output():
    ci_script = os.path.join(PROJECT_DIR, 'ci.sh')

    # Run the CI script
    result = subprocess.run(['bash', ci_script], cwd=PROJECT_DIR, capture_output=True)
    assert result.returncode == 0, f"ci.sh failed with exit code {result.returncode}.\nStdout: {result.stdout.decode()}\nStderr: {result.stderr.decode()}"

    output_file = os.path.join(PROJECT_DIR, 'output.json')
    assert os.path.isfile(output_file), f"{output_file} was not generated"

    with open(output_file, 'r') as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"{output_file} does not contain valid JSON.\nContent:\n{content}")

    assert data.get("status") == "resolved_correctly", f"Expected status 'resolved_correctly', got {data.get('status')}"

def test_semver_cpp_fixed():
    semver_file = os.path.join(PROJECT_DIR, 'semver.cpp')
    assert os.path.isfile(semver_file), f"{semver_file} does not exist"

    with open(semver_file, 'r') as f:
        content = f.read()

    # The buggy code used a > b ? 1 : -1
    assert 'a > b ? 1 : -1' not in content, "Buggy string comparison still exists in semver.cpp"