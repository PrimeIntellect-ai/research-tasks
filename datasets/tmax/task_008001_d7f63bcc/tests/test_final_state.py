# test_final_state.py

import os
import subprocess
import pytest

def get_dir_size(path):
    """Calculate total size of a directory."""
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def test_deploy_proxy_c_exists():
    """Verify that the C source file exists."""
    path = "/home/user/deploy_proxy.c"
    assert os.path.isfile(path), f"Expected C source file {path} does not exist."

def test_deploy_proxy_executable_exists():
    """Verify that the compiled C program exists and is executable."""
    path = "/home/user/deploy_proxy"
    assert os.path.isfile(path), f"Expected executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_optimize_storage_sh_exists():
    """Verify that the bash script exists and is executable."""
    path = "/home/user/optimize_storage.sh"
    assert os.path.isfile(path), f"Expected bash script {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_proxy_backend_conf_correctness():
    """Verify that the proxy backend configuration is generated correctly based on current disk usage."""
    caches = {
        "cache_a": {"path": "/home/user/cache_a", "port": "8081"},
        "cache_b": {"path": "/home/user/cache_b", "port": "8082"},
        "cache_c": {"path": "/home/user/cache_c", "port": "8083"}
    }

    # Calculate sizes to find the smallest
    sizes = {}
    for name, info in caches.items():
        if os.path.isdir(info["path"]):
            # Using du -sb to match bash script behavior closely
            try:
                output = subprocess.check_output(['du', '-sb', info["path"]]).decode('utf-8')
                size = int(output.split()[0])
            except Exception:
                size = get_dir_size(info["path"])
            sizes[name] = size
        else:
            sizes[name] = float('inf')

    smallest_cache = min(sizes, key=sizes.get)
    expected_port = caches[smallest_cache]["port"]

    expected_content = f"backend best_cache {{ server 127.0.0.1:{expected_port}; }}\n"
    conf_path = "/home/user/proxy_backend.conf"

    assert os.path.isfile(conf_path), f"Configuration file {conf_path} does not exist. Did you run the script?"

    with open(conf_path, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        f"Contents of {conf_path} are incorrect.\n"
        f"Expected:\n{repr(expected_content)}\n"
        f"Actual:\n{repr(actual_content)}\n"
        f"Smallest cache was determined to be {smallest_cache}."
    )