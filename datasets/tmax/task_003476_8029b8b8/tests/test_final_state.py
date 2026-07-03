# test_final_state.py

import os
import subprocess
import pytest

def test_topo_sh_exists_and_executable():
    topo_sh_path = '/home/user/pipeline/topo.sh'
    assert os.path.isfile(topo_sh_path), f"{topo_sh_path} does not exist."
    assert os.access(topo_sh_path, os.X_OK), f"{topo_sh_path} is not executable."

def test_topo_sh_no_python_or_perl():
    topo_sh_path = '/home/user/pipeline/topo.sh'
    with open(topo_sh_path, 'r') as f:
        content = f.read().lower()

    assert 'python' not in content, f"{topo_sh_path} contains 'python', which is not allowed."
    assert 'perl' not in content, f"{topo_sh_path} contains 'perl', which is not allowed."

def test_test_results_log_exists_and_correct():
    log_path = '/home/user/pipeline/test_results.log'
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you run 'make test'?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected = "INIT_SUCCESS: 35"
    assert expected in content, f"Expected '{expected}' in {log_path}, but got '{content}'"

def test_topo_sh_output_format():
    topo_sh_path = '/home/user/pipeline/topo.sh'
    deps_txt_path = '/home/user/pipeline/deps.txt'

    try:
        result = subprocess.run(
            [topo_sh_path, deps_txt_path],
            cwd='/home/user/pipeline',
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {topo_sh_path} failed with error: {e.stderr}")

    modules = output.split()
    expected_modules = {'module_main', 'module_ui', 'module_auth', 'module_crypto', 'module_core'}

    assert set(modules) == expected_modules, "The output of topo.sh does not contain all the required modules."
    assert len(modules) == len(expected_modules), "The output of topo.sh contains duplicate or extra modules."