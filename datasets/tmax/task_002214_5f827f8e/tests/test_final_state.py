# test_final_state.py

import os
import re
import time
import subprocess
import pytest

def test_directories_and_files():
    certs_dir = "/home/user/certs"
    www_dir = "/home/user/www"

    assert os.path.isdir(certs_dir), f"Directory {certs_dir} does not exist"
    assert os.path.isdir(www_dir), f"Directory {www_dir} does not exist"

    crt_path = os.path.join(certs_dir, "server.crt")
    key_path = os.path.join(certs_dir, "server.key")

    assert os.path.isfile(crt_path), f"File {crt_path} does not exist"
    assert os.path.isfile(key_path), f"File {key_path} does not exist"

    active_crt = os.path.join(certs_dir, "active.crt")
    active_key = os.path.join(certs_dir, "active.key")

    assert os.path.islink(active_crt), f"{active_crt} is not a symlink"
    assert os.path.islink(active_key), f"{active_key} is not a symlink"

    assert os.readlink(active_crt) == "server.crt" or os.path.abspath(os.path.join(certs_dir, os.readlink(active_crt))) == os.path.abspath(crt_path), "active.crt does not point to server.crt"
    assert os.readlink(active_key) == "server.key" or os.path.abspath(os.path.join(certs_dir, os.readlink(active_key))) == os.path.abspath(key_path), "active.key does not point to server.key"

    target_html = os.path.join(www_dir, "target.html")
    index_html = os.path.join(www_dir, "index.html")

    assert os.path.isfile(target_html), f"File {target_html} does not exist"
    with open(target_html, "r") as f:
        content = f.read()
    assert content == "NETWORK_OK", f"target.html content is '{content}', expected 'NETWORK_OK'"

    assert os.path.islink(index_html), f"{index_html} is not a symlink"
    assert os.readlink(index_html) == "target.html" or os.path.abspath(os.path.join(www_dir, os.readlink(index_html))) == os.path.abspath(target_html), "index.html does not point to target.html"

def test_bashrc_exports():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist"

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert re.search(r"^export\s+WWW_PORT=8080", content, re.MULTILINE), "WWW_PORT=8080 export not found in .bashrc"
    assert re.search(r"^export\s+CERT_PATH=/home/user/certs/active\.crt", content, re.MULTILINE), "CERT_PATH export not found in .bashrc"

def test_server_performance():
    server_path = "/home/user/server"
    assert os.path.isfile(server_path), f"Server binary {server_path} does not exist"
    assert os.access(server_path, os.X_OK), f"Server binary {server_path} is not executable"

    # Start the server
    server_proc = subprocess.Popen([server_path])
    time.sleep(1)  # Wait for server to bind

    try:
        # Run the benchmark
        bench_out = subprocess.check_output(["/app/bench", "localhost", "8080"], text=True)

        # Extract the metric
        match = re.search(r"Requests per second:\s+([0-9.]+)", bench_out)
        assert match, f"Metric extraction failed. Output was: {bench_out}"

        rps = float(match.group(1))

        # Threshold check
        assert rps >= 5000.0, f"Server performance too low. Achieved {rps} RPS, expected >= 5000.0"
    finally:
        server_proc.terminate()
        server_proc.wait(timeout=2)