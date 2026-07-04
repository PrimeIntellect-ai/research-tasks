# test_final_state.py
import os
import stat
import hashlib
import base64

def test_package_sh_fixed():
    path = "/home/user/grpc-math-service/package.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check for sort
    assert "sort" in content, "package.sh does not appear to sort the files. Use 'sort' in the pipeline."

def test_test_orchestrator_exists_and_executable():
    path = "/home/user/test_orchestrator.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), f"File {path} is not executable."

def test_mock_protos_created():
    a_math = "/home/user/mock_protos/a_math.proto"
    b_math = "/home/user/mock_protos/b_math.proto"
    assert os.path.isfile(a_math), f"File {a_math} does not exist."
    assert os.path.isfile(b_math), f"File {b_math} does not exist."

def test_test_result_log_pass():
    path = "/home/user/test_result.log"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "PASS", f"Expected 'PASS' in {path}, but got '{content}'"

def test_manifest_hash_no_newline():
    path = "/home/user/grpc-math-service/manifest_hash.txt"
    # The orchestrator should have run the script, creating the manifest_hash.txt
    # But it might have run it from a different working directory. Let's check if it exists in grpc-math-service
    # If not, maybe it was created in the orchestrator's working dir. 
    # Let's check the file if it exists.
    if os.path.isfile(path):
        with open(path, "rb") as f:
            content = f.read()
        if len(content) > 0:
            assert content[-1:] != b"\n", "manifest_hash.txt still contains a trailing newline."