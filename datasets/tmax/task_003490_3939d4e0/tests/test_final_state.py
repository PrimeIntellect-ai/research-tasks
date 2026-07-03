# test_final_state.py
import os
import stat
import py_compile

def test_fix_and_run_script_exists_and_valid():
    script_path = "/home/user/fix_and_run.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    try:
        py_compile.compile(script_path, doraise=True)
    except Exception as e:
        assert False, f"The script {script_path} contains invalid Python syntax: {e}"

def test_deploy_sh_content():
    deploy_path = "/home/user/app/deploy.sh"
    assert os.path.isfile(deploy_path), f"The script {deploy_path} does not exist."

    with open(deploy_path, "r") as f:
        content = f.read().strip()

    expected_content = "#!/bin/bash\n/usr/bin/python3 /home/user/app/worker.py > /home/user/app/deploy.log"
    assert content == expected_content, f"The content of {deploy_path} is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_deploy_sh_permissions():
    deploy_path = "/home/user/app/deploy.sh"
    assert os.path.isfile(deploy_path), f"The script {deploy_path} does not exist."

    st = os.stat(deploy_path)
    perms = oct(st.st_mode)[-3:]
    assert perms == "755", f"Permissions for {deploy_path} are {perms}, but should be 755."

def test_deploy_log_content():
    log_path = "/home/user/app/deploy.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist. Did the script run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "Worker updated successfully."
    assert content == expected_content, f"The content of {log_path} is incorrect. Expected '{expected_content}', got '{content}'"