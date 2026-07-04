# test_final_state.py
import os
import subprocess
import re
import tempfile

def test_compute_sig_exists_and_executable():
    path = "/home/user/compute_sig.sh"
    assert os.path.isfile(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_compute_sig_logic():
    path = "/home/user/compute_sig.sh"

    # Test case 1: "hello"
    with tempfile.NamedTemporaryFile(delete=False) as f1:
        f1.write(b"hello")
        f1_name = f1.name

    try:
        result = subprocess.run([path, f1_name], capture_output=True, text=True)
        assert result.returncode == 0, f"{path} failed on execution"
        assert result.stdout.strip() == "20", f"Expected signature 20 for 'hello', got {result.stdout.strip()}"
    finally:
        os.remove(f1_name)

    # Test case 2: "\x01\x02\xFF"
    with tempfile.NamedTemporaryFile(delete=False) as f2:
        f2.write(b"\x01\x02\xFF")
        f2_name = f2.name

    try:
        result = subprocess.run([path, f2_name], capture_output=True, text=True)
        assert result.returncode == 0, f"{path} failed on execution"
        assert result.stdout.strip() == "2", f"Expected signature 2 for '\\x01\\x02\\xFF', got {result.stdout.strip()}"
    finally:
        os.remove(f2_name)

def test_file_service_proto():
    path = "/home/user/file_service.proto"
    assert os.path.isfile(path), f"{path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    # Check syntax
    assert re.search(r'syntax\s*=\s*"proto3"\s*;', content), "Missing or incorrect syntax declaration"

    # Check package
    assert re.search(r'package\s+fileorg\s*;', content), "Missing or incorrect package declaration"

    # Check service
    assert re.search(r'service\s+FileOrganizer\s*\{', content), "Missing FileOrganizer service"
    assert re.search(r'rpc\s+ComputeSignature\s*\(\s*FileRequest\s*\)\s*returns\s*\(\s*SignatureResponse\s*\)', content), "Missing or incorrect ComputeSignature rpc"

    # Check messages
    assert re.search(r'message\s+FileRequest\s*\{', content), "Missing FileRequest message"
    assert re.search(r'string\s+filepath\s*=\s*1\s*;', content), "Missing or incorrect filepath field in FileRequest"

    assert re.search(r'message\s+SignatureResponse\s*\{', content), "Missing SignatureResponse message"
    assert re.search(r'uint32\s+signature\s*=\s*1\s*;', content), "Missing or incorrect signature field in SignatureResponse"

def test_prop_test_exists_and_executable():
    path = "/home/user/prop_test.sh"
    assert os.path.isfile(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_prop_test_execution():
    path = "/home/user/prop_test.sh"
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} exited with code {result.returncode}"
    assert "PASS" in result.stdout, f"Expected 'PASS' in output, got {result.stdout}"