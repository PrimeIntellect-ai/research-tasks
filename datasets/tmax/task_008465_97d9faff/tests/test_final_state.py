# test_final_state.py

import os
import stat
import pytest

EDGE_DIR = "/home/user/edge"

def test_sensor_go_port_updated():
    path = os.path.join(EDGE_DIR, "sensor.go")
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, "r") as f:
        content = f.read()
    assert "127.0.0.1:9091" in content, f"Port in {path} was not updated to match collector.go (9091)"

def test_init_sh_exists_and_executable():
    path = os.path.join(EDGE_DIR, "init.sh")
    assert os.path.isfile(path), f"{path} is missing"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable"

def test_binaries_compiled():
    for binary in ["sensor", "collector", "quota"]:
        path = os.path.join(EDGE_DIR, "bin", binary)
        assert os.path.isfile(path), f"Compiled binary {path} is missing"
        st = os.stat(path)
        assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable"
        with open(path, "rb") as f:
            magic = f.read(4)
            assert magic == b"\x7fELF", f"{path} is not a valid ELF binary"

def test_quota_enforcement():
    old_log = os.path.join(EDGE_DIR, "logs", "old_sys.log")
    recent_log = os.path.join(EDGE_DIR, "logs", "recent_errors.log")

    assert not os.path.exists(old_log), f"{old_log} was not deleted by the quota enforcement"
    assert os.path.isfile(recent_log), f"{recent_log} should not have been deleted"

def test_process_sh_exists_and_executable():
    path = os.path.join(EDGE_DIR, "process.sh")
    assert os.path.isfile(path), f"{path} is missing"
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable"

def test_error_summary_output():
    path = os.path.join(EDGE_DIR, "error_summary.txt")
    assert os.path.isfile(path), f"{path} is missing"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "401: 1\n404: 2\n502: 3"
    assert content == expected, f"Contents of {path} do not match the expected summary.\nExpected:\n{expected}\nGot:\n{content}"