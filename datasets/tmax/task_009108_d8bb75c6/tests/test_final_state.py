# test_final_state.py

import os
import re
import pytest

def test_worker_c_fixed():
    filepath = "/home/user/polybuild/c_src/worker.c"
    assert os.path.isfile(filepath), f"File {filepath} is missing"
    with open(filepath, "r") as f:
        content = f.read()

    # Check that the off-by-one error is fixed
    # The original was i <= 5. The fix should be i < 5 or i <= 4.
    assert "i <= 5" not in content, "worker.c still contains the out-of-bounds loop condition 'i <= 5'"
    assert re.search(r'i\s*<\s*5', content) or re.search(r'i\s*<=\s*4', content), "worker.c does not contain the corrected loop condition (e.g., 'i < 5')"

def test_test_results_log():
    filepath = "/home/user/test_results.log"
    assert os.path.isfile(filepath), f"File {filepath} is missing. Did you run the tests and redirect the output?"
    with open(filepath, "r") as f:
        content = f.read()

    assert "PASS" in content, "test_results.log does not contain 'PASS'. The Go tests may have failed or not run correctly."

def test_go_mod_exists_and_requires_websocket():
    filepath = "/home/user/polybuild/go_src/go.mod"
    assert os.path.isfile(filepath), f"File {filepath} is missing. Did you initialize the Go module?"
    with open(filepath, "r") as f:
        content = f.read()

    assert "github.com/gorilla/websocket" in content, "go.mod does not require github.com/gorilla/websocket"

def test_builder_test_go_implementation():
    filepath = "/home/user/polybuild/go_src/builder_test.go"
    assert os.path.isfile(filepath), f"File {filepath} is missing"
    with open(filepath, "r") as f:
        content = f.read()

    assert "httptest.NewServer" in content, "builder_test.go does not contain httptest.NewServer to mock the server"
    assert "Upgrade" in content or "Upgrader" in content, "builder_test.go does not appear to upgrade the HTTP connection to a WebSocket"