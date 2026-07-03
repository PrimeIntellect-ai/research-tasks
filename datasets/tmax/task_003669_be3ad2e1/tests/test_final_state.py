# test_final_state.py
import os
import stat
import pytest

def test_tls_certs_exist():
    cert_path = "/home/user/tls_web/cert.pem"
    key_path = "/home/user/tls_web/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Key file {key_path} does not exist."

def test_git_hook_executable():
    hook_path = "/home/user/monitor.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Git hook {hook_path} is not executable."

def test_deployed_files_exist():
    checker_c = "/home/user/monitor_deploy/checker.c"
    checker_bin = "/home/user/monitor_deploy/checker"
    assert os.path.isfile(checker_c), f"Deployed source {checker_c} does not exist."
    assert os.path.isfile(checker_bin), f"Compiled binary {checker_bin} does not exist."
    st = os.stat(checker_bin)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled binary {checker_bin} is not executable."

def test_hook_output_log():
    log_path = "/home/user/hook_output.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "STATUS: 200" in content, f"Log file {log_path} does not contain 'STATUS: 200'."