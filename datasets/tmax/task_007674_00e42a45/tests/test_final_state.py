# test_final_state.py

import os
import stat
import urllib.request
import urllib.error
import pytest

def test_final_result_file():
    path = '/home/user/final_result.txt'
    assert os.path.isfile(path), f"File {path} does not exist. The script must create this file."

    with open(path, 'r') as f:
        content = f.read().strip()

    expected = "4729:Tok_99182:FLAG{privesc_base64_succ3ss}"
    assert content == expected, f"Content of {path} is incorrect. Expected '{expected}', got '{content}'."

def test_solve_script_exists_and_executable():
    path = '/home/user/solve.sh'
    assert os.path.isfile(path), f"File {path} does not exist. The exploit script is missing."

    st = os.stat(path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"File {path} is not executable. The script must have execute permissions."

def test_server_is_cleaned_up():
    # The script should have terminated the background Python server.
    # We can test this by attempting to connect to localhost:5000
    server_running = False
    try:
        urllib.request.urlopen("http://127.0.0.1:5000/", timeout=1)
        server_running = True
    except urllib.error.URLError as e:
        # Connection refused means the server is down, which is expected
        pass
    except Exception:
        # Other exceptions might occur, but generally we want it to fail to connect
        pass

    assert not server_running, "The Python server on port 5000 is still running. The script must terminate it before exiting."