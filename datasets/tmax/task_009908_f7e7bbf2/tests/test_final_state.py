# test_final_state.py

import os
import subprocess
import stat
import pytest

def test_files_exist():
    assert os.path.isfile('/home/user/transform.c'), "transform.c is missing."
    assert os.path.isfile('/home/user/build.sh'), "build.sh is missing."
    assert os.path.isfile('/home/user/libtransform.so'), "libtransform.so is missing."
    assert os.path.isfile('/home/user/result.log'), "result.log is missing."

def test_build_sh_executable():
    st = os.stat('/home/user/build.sh')
    assert bool(st.st_mode & stat.S_IXUSR), "build.sh is not executable."

def test_initial_result_log():
    with open('/home/user/result.log', 'r') as f:
        content = f.read().strip()
    assert content == "13,PROD_reenigne", f"Expected '13,PROD_reenigne' in result.log, got '{content}'"

def test_build_ci_env():
    # Run build.sh with CI
    res = subprocess.run(['/home/user/build.sh', 'CI'], capture_output=True, text=True)
    assert res.returncode == 0, f"build.sh failed with CI argument: {res.stderr}"

    # Run verify.py
    res = subprocess.run(['python3', '/home/user/verify.py'], capture_output=True, text=True)
    assert res.returncode == 0, f"verify.py failed: {res.stderr}"

    with open('/home/user/result.log', 'r') as f:
        content = f.read().strip()
    assert content == "11,CI_reenigne", f"Expected '11,CI_reenigne' in result.log, got '{content}'"

def test_build_default_env():
    # Compile manually without PIPELINE_ENV
    res = subprocess.run([
        'gcc', '-shared', '-fPIC', '-o', '/home/user/libtransform.so', '/home/user/transform.c'
    ], capture_output=True, text=True)
    assert res.returncode == 0, f"Manual compilation failed: {res.stderr}"

    # Run verify.py
    res = subprocess.run(['python3', '/home/user/verify.py'], capture_output=True, text=True)
    assert res.returncode == 0, f"verify.py failed: {res.stderr}"

    with open('/home/user/result.log', 'r') as f:
        content = f.read().strip()
    assert content == "16,DEFAULT_reenigne", f"Expected '16,DEFAULT_reenigne' in result.log, got '{content}'"