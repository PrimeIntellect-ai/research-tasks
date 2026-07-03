# test_final_state.py

import os
import stat
import ssl
import urllib.request
import time

def test_compilation():
    setup_bin = '/home/user/bin/setup'
    assert os.path.isfile(setup_bin), f"Compiled binary {setup_bin} does not exist."
    st = os.stat(setup_bin)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {setup_bin} is not executable."

def test_directories_and_symlink():
    dirs = [
        '/home/user/deploy/webroot',
        '/home/user/deploy/certs',
        '/home/user/shared_assets'
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

    symlink = '/home/user/deploy/webroot/assets'
    assert os.path.islink(symlink), f"{symlink} is not a symlink."
    assert os.readlink(symlink) == '/home/user/shared_assets', f"Symlink {symlink} does not point to /home/user/shared_assets."

    test_file = '/home/user/shared_assets/test.txt'
    assert os.path.isfile(test_file), f"Test file {test_file} does not exist."
    with open(test_file, 'r') as f:
        content = f.read().strip()
    assert content == "Assets working", f"Test file content is incorrect: {content}"

def test_expect_script_and_db():
    expect_script = '/home/user/bin/run_setup.exp'
    assert os.path.isfile(expect_script), f"Expect script {expect_script} does not exist."

    db_file = '/home/user/deploy/users.db'
    assert os.path.isfile(db_file), f"Database file {db_file} does not exist."
    with open(db_file, 'r') as f:
        content = f.read()
    assert "USER:app_admin|PASS:SecureDeploy2024" in content, "Database file does not contain the expected user and password."

def test_tls_certs():
    cert_file = '/home/user/deploy/certs/cert.pem'
    key_file = '/home/user/deploy/certs/key.pem'
    assert os.path.isfile(cert_file), f"Certificate file {cert_file} does not exist."
    assert os.path.isfile(key_file), f"Key file {key_file} does not exist."

def test_web_server():
    url = "https://localhost:8443/assets/test.txt"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.urlopen(url, context=ctx, timeout=5)
        content = req.read().decode('utf-8').strip()
        assert "Assets working" in content, "Web server did not return the expected content from the symlinked directory."
    except Exception as e:
        assert False, f"Failed to connect to the web server or retrieve the file: {e}"