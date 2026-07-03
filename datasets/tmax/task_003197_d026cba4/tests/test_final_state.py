# test_final_state.py

import os
import re

def test_test_results_exists_and_correct():
    path = "/home/user/test_results.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the integration test?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "55", f"Expected test_results.txt to contain '55', but got '{content}'. The math logic or proxy might not be working correctly."

def test_rust_backend_built():
    path = "/home/user/rust_backend/target/release/rust_backend"
    assert os.path.isfile(path), f"Compiled Rust binary {path} is missing. Did you run 'cargo build --release'?"

def test_patch_applied():
    path = "/home/user/rust_backend/src/main.rs"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "if n <= 1" in content, "The patch does not seem to be applied to src/main.rs."

def test_proxy_python3_syntax():
    path = "/home/user/proxy.py"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check that Python 2 syntax was removed or updated
    assert not re.search(r"except Exception,\s*e:", content), "Found Python 2 exception syntax in proxy.py."
    assert not re.search(r"print\s+[\"']", content), "Found Python 2 print statement in proxy.py."
    assert "http.server" in content or "urllib.request" in content, "proxy.py does not seem to use Python 3 modules (e.g., http.server, urllib.request)."