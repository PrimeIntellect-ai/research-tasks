# test_final_state.py

import os
import json
import tarfile
import hashlib
import urllib.request
import urllib.error
import pytest

PROJECT_DIR = "/home/user/project"
BUILD_DIR = os.path.join(PROJECT_DIR, "build")
ARTIFACTS_DIR = os.path.join(PROJECT_DIR, "artifacts")

def test_build_order():
    build_order_path = os.path.join(PROJECT_DIR, "build_order.txt")
    assert os.path.isfile(build_order_path), f"Build order file missing: {build_order_path}"

    with open(build_order_path, "r") as f:
        content = f.read().strip()

    expected_order = "math_ops,transform,test_integration"
    assert content == expected_order, f"Expected build order '{expected_order}', but got '{content}'"

def test_shared_libraries():
    lib_math = os.path.join(BUILD_DIR, "libmath_ops.so")
    lib_transform = os.path.join(BUILD_DIR, "libtransform.so")

    for lib in [lib_math, lib_transform]:
        assert os.path.isfile(lib), f"Shared library missing: {lib}"
        with open(lib, "rb") as f:
            magic = f.read(4)
            assert magic == b"\x7fELF", f"File {lib} is not a valid ELF file"

def test_release_tarball():
    tarball_path = os.path.join(ARTIFACTS_DIR, "release.tar.gz")
    assert os.path.isfile(tarball_path), f"Tarball missing: {tarball_path}"

    expected_files = {"libmath_ops.so", "libtransform.so", "test_integration.py"}

    with tarfile.open(tarball_path, "r:gz") as tar:
        members = [os.path.basename(m.name) for m in tar.getmembers() if m.isfile()]
        for ef in expected_files:
            assert ef in members, f"File {ef} is missing from the release tarball"

def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_manifest_json():
    manifest_path = os.path.join(ARTIFACTS_DIR, "manifest.json")
    assert os.path.isfile(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    expected_keys = ["libmath_ops.so", "libtransform.so", "test_integration.py"]
    for key in expected_keys:
        assert key in manifest, f"Key {key} missing from manifest.json"

    # Verify hashes
    lib_math = os.path.join(BUILD_DIR, "libmath_ops.so")
    lib_transform = os.path.join(BUILD_DIR, "libtransform.so")
    test_integration = os.path.join(PROJECT_DIR, "test_integration.py")

    assert manifest["libmath_ops.so"] == compute_sha256(lib_math), "Hash mismatch for libmath_ops.so"
    assert manifest["libtransform.so"] == compute_sha256(lib_transform), "Hash mismatch for libtransform.so"
    assert manifest["test_integration.py"] == compute_sha256(test_integration), "Hash mismatch for test_integration.py"

def test_http_server_and_pid():
    pid_path = os.path.join(ARTIFACTS_DIR, "server.pid")
    assert os.path.isfile(pid_path), f"PID file missing: {pid_path}"

    with open(pid_path, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"
    pid = int(pid_str)

    # Check if process exists
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running")

    # Check if HTTP server is serving the artifacts
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/manifest.json", timeout=2)
        content = req.read()
        assert req.status == 200, "HTTP server did not return 200 OK for manifest.json"

        # Verify content matches local file
        with open(os.path.join(ARTIFACTS_DIR, "manifest.json"), "rb") as f:
            local_content = f.read()

        assert content == local_content, "HTTP server served incorrect content for manifest.json"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to HTTP server on port 8080: {e}")