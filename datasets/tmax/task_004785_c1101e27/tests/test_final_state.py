# test_final_state.py

import os
import socket
import stat

def test_bin_service_compiled():
    path = "/home/user/bin/service"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist. Did you compile the C code?"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {path} is not executable."

def test_log_file_correct():
    path = "/home/user/data_spool/service.log"
    assert os.path.isfile(path), f"Log file {path} does not exist. Did the service run and write to the correct path?"

    with open(path, 'r') as f:
        content = f.read()

    expected_string = "[INIT] Service started in timezone: UTC"
    assert expected_string in content, f"Log file {path} does not contain the expected string. Found: {content}"

def test_port_8888_listening():
    # Check if port 8888 is listening on localhost
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex(('127.0.0.1', 8888))
        assert result == 0, "Port 8888 is not listening. The SSH tunnel might not be running or configured correctly."
    finally:
        s.close()

def test_run_service_sh_contents():
    path = "/home/user/run_service.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "TZ=UTC" in content, "Script does not export TZ=UTC."
    assert "LOG_FILE_PATH=/home/user/data_spool/service.log" in content, "Script does not export LOG_FILE_PATH correctly."
    assert "ssh " in content and "8888:127.0.0.1:9999" in content, "Script does not contain the correct SSH port forwarding command."
    assert "-N" in content and "-f" in content, "SSH command must use -N and -f flags."
    assert "/home/user/bin/service" in content, "Script does not launch the compiled service."

def test_c_code_updated():
    path = "/home/user/src/service.c"
    assert os.path.isfile(path), f"C source file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "getenv" in content, "C code does not appear to use getenv() to read LOG_FILE_PATH."
    assert "/var/log/service.log" not in content, "C code still contains the hardcoded broken log path."