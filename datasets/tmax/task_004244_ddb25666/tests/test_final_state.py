# test_final_state.py

import os
import socket
import stat
import time
import pytest

def test_daemon_files_exist():
    """Verify that the C source file and executable exist."""
    c_file = "/home/user/prov_daemon.c"
    executable = "/home/user/prov_daemon"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."
    assert os.path.isfile(executable), f"Executable {executable} is missing."

def test_daemon_protocol_and_acl_creation():
    """Connect to the daemon, send the passcode, check the response and the resulting ACL file."""
    acl_file = "/home/user/qemu_vnc.acl"

    # Remove the ACL file if it exists to ensure the daemon creates it
    if os.path.exists(acl_file):
        os.chmod(acl_file, 0o666)
        os.remove(acl_file)

    passcode = b"purple dinosaur\n"

    # Connect to the daemon
    try:
        with socket.create_connection(('127.0.0.1', 8111), timeout=5) as s:
            s.sendall(passcode)
            response = s.recv(1024)
    except ConnectionRefusedError:
        pytest.fail("Daemon is not listening on 127.0.0.1:8111.")
    except Exception as e:
        pytest.fail(f"Failed to communicate with daemon: {e}")

    expected_response = b"VNC_ACL_UPDATED\n"
    assert response == expected_response, f"Expected response {expected_response}, got {response}"

    # Give the daemon a moment to write the file
    time.sleep(0.5)

    assert os.path.isfile(acl_file), f"ACL file {acl_file} was not created by the daemon."

    with open(acl_file, 'r') as f:
        contents = f.read()

    assert contents == "VNC_ACCESS=GRANTED\n", f"ACL file contents incorrect. Got: {repr(contents)}"

    # Check permissions
    st = os.stat(acl_file)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"ACL file permissions should be 0400, got {oct(perms)}"