# test_final_state.py
import os
import subprocess

def test_fix_patch_exists_and_valid():
    patch_path = "/home/user/gateway/fix.patch"
    assert os.path.isfile(patch_path), f"{patch_path} is missing"
    with open(patch_path, "r") as f:
        content = f.read()
    assert "---" in content and "+++" in content, f"{patch_path} does not look like a unified diff"

def test_router_prop_test_exists_and_valid():
    test_path = "/home/user/gateway/router_prop_test.go"
    assert os.path.isfile(test_path), f"{test_path} is missing"
    with open(test_path, "r") as f:
        content = f.read()
    assert "testing/quick" in content, f"{test_path} does not import 'testing/quick'"
    assert "func Test" in content, f"{test_path} does not contain a test function"

def test_test_results_log_exists():
    log_path = "/home/user/gateway/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} is missing"
    with open(log_path, "r") as f:
        content = f.read()
    assert "PASS" in content, f"{log_path} does not contain 'PASS'"

def test_router_is_fixed():
    hidden_test_path = "/home/user/gateway/hidden_verify_test.go"
    hidden_test_content = """package gateway_test

import (
\t"gateway"
\t"testing"
)

func TestStrictConstraint(t *testing.T) {
\tr := gateway.NewRouter()
\tr.Register("/users/{id:int}", "userHandler")
\t
\t_, _, ok := r.Match("/users/123a")
\tif ok {
\t\tt.Errorf("Expected /users/123a to NOT match, but it did")
\t}

\t_, _, ok = r.Match("/users/123")
\tif !ok {
\t\tt.Errorf("Expected /users/123 to match, but it didn't")
\t}
}
"""
    try:
        with open(hidden_test_path, "w") as f:
            f.write(hidden_test_content)

        result = subprocess.run(
            ["go", "test", "-v", "-run", "TestStrictConstraint"],
            cwd="/home/user/gateway",
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Hidden verification test failed, indicating the bug is not properly fixed:\n{result.stdout}\n{result.stderr}"
    finally:
        if os.path.exists(hidden_test_path):
            os.remove(hidden_test_path)