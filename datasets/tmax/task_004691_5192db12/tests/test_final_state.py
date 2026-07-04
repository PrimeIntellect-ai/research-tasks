# test_final_state.py
import os
import stat
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/fetch_deps.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Script {script_path} is not executable."

def test_build_log_content():
    log_path = "/home/user/build.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "SUCCESS: requests",
        "SUCCESS: serde",
        "CHECKSUM_FAILED: lodash",
        "NOT_FOUND: gin"
    ]

    assert lines == expected_lines, f"Log file {log_path} contents do not match expected output. Got: {lines}"

def test_build_cache_contents():
    cache_dir = "/home/user/build_cache"
    assert os.path.isdir(cache_dir), f"Cache directory {cache_dir} does not exist."

    requests_path = os.path.join(cache_dir, "requests")
    serde_path = os.path.join(cache_dir, "serde")
    lodash_path = os.path.join(cache_dir, "lodash")
    gin_path = os.path.join(cache_dir, "gin")

    assert os.path.isfile(requests_path), f"Dependency {requests_path} is missing."
    assert os.path.isfile(serde_path), f"Dependency {serde_path} is missing."
    assert not os.path.exists(lodash_path), f"Dependency {lodash_path} should not exist."
    assert not os.path.exists(gin_path), f"Dependency {gin_path} should not exist."