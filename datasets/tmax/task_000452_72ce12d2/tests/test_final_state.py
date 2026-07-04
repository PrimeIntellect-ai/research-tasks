# test_final_state.py

import os
import stat
import subprocess
import pytest

RELEASE_DIR = "/home/user/release"
BUILD_SCRIPT = os.path.join(RELEASE_DIR, "build_release.sh")
LOCKFILE = os.path.join(RELEASE_DIR, "lockfile.txt")
WAF_ROUTER = os.path.join(RELEASE_DIR, "waf_router.sh")

def test_build_script_exists_and_executable():
    assert os.path.isfile(BUILD_SCRIPT), f"Build script not found at {BUILD_SCRIPT}"
    st = os.stat(BUILD_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Build script {BUILD_SCRIPT} is not executable"

def test_lockfile_content():
    assert os.path.isfile(LOCKFILE), f"Lockfile not found at {LOCKFILE}. Did the build script run?"
    with open(LOCKFILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "auth=1.0.0",
        "db=1.0.0",
        "logger=1.0.0"
    ]
    assert lines == expected, f"Lockfile content incorrect. Expected {expected}, got {lines}"

def test_waf_router_exists_and_executable():
    assert os.path.isfile(WAF_ROUTER), f"WAF router script not found at {WAF_ROUTER}"
    st = os.stat(WAF_ROUTER)
    assert bool(st.st_mode & stat.S_IXUSR), f"WAF router script {WAF_ROUTER} is not executable"

def run_waf_router(method, path, query_string=""):
    result = subprocess.run(
        [WAF_ROUTER, method, path, query_string],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

@pytest.mark.parametrize("method, path, query_string, expected", [
    ("POST", "/login", "username=admin&password=123", "ROUTED_TO: auth"),
    ("POST", "/login", "username=admin&password=123&token=abc", "ROUTED_TO: auth"),
    ("POST", "/login", "username=admin&password=123&mfa=1", "403 FORBIDDEN"),
    ("GET", "/data", "limit=10", "ROUTED_TO: db"),
    ("POST", "/data", "query=select&limit=5", "ROUTED_TO: db"),
    ("GET", "/data", "limit=10&offset=5", "403 FORBIDDEN"),
    ("GET", "/logs", "", "ROUTED_TO: logger"),
    ("GET", "/logs", "date=2023-10-01", "ROUTED_TO: logger"),
    ("PUT", "/logs", "", "403 FORBIDDEN"),
    ("GET", "/unknown", "", "403 FORBIDDEN"),
    ("POST", "/login", "unknown_param=1", "403 FORBIDDEN"),
])
def test_waf_router_behavior(method, path, query_string, expected):
    output = run_waf_router(method, path, query_string)
    assert output == expected, f"WAF router failed for {method} {path} '{query_string}'. Expected '{expected}', got '{output}'"