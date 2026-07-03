# test_final_state.py

import os
import pytest
import stat

def test_fix_and_test_script_exists_and_executable():
    path = "/home/user/fix_and_test.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {path} is not executable."

def test_proto_file_fixed():
    path = "/home/user/api-gateway/proto/service.proto"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()
    assert "int32 id = 1;" in content, "Proto file was not fixed; 'int32 id = 1;' not found."
    assert "integer id = 1;" not in content, "Proto file still contains the syntax error 'integer id = 1;'."

def test_build_rs_created():
    path = "/home/user/api-gateway/build.rs"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()
    assert 'tonic_build::compile_protos("proto/service.proto")?' in content, "build.rs does not contain the required tonic_build command."

def test_main_rs_fixed():
    path = "/home/user/api-gateway/src/main.rs"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()
    assert "get_record(req.id);" in content, "main.rs was not fixed; 'get_record(req.id);' not found."
    assert "fetch_record(req.id);" not in content, "main.rs still contains the typo 'fetch_record(req.id);'."

def test_project_compiled():
    path = "/home/user/api-gateway/target/debug/api-gateway"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist. The project may not have compiled successfully."

def test_test_results_log():
    path = "/home/user/test_results.log"
    assert os.path.isfile(path), f"Log file {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert "Successful requests: 50" in content, f"Expected 'Successful requests: 50' in {path}, but got: {content}"