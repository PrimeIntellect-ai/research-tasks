# test_final_state.py

import os
import re

def test_request_proto_fixed():
    request_proto_path = "/home/user/rpc_utility/schemas/request.proto"
    assert os.path.isfile(request_proto_path), f"File missing: {request_proto_path}"

    with open(request_proto_path, "r") as f:
        content = f.read()

    assert 'import "user.proto";' not in content, "Circular import 'import \"user.proto\";' was not removed from request.proto"
    assert re.search(r'int32\s+owner_id\s*=\s*2\s*;', content), "Field 'int32 owner_id = 2;' not found in request.proto"
    assert "User owner" not in content, "'User owner' field was not removed from request.proto"

def test_generated_c_files_exist():
    src_dir = "/home/user/rpc_utility/src"
    expected_files = [
        "user.pb-c.c", "user.pb-c.h",
        "request.pb-c.c", "request.pb-c.h",
        "batch.pb-c.c", "batch.pb-c.h"
    ]
    for f in expected_files:
        path = os.path.join(src_dir, f)
        assert os.path.isfile(path), f"Generated protobuf-c file missing: {path}"

def test_processor_source_exists():
    processor_c_path = "/home/user/rpc_utility/src/processor.c"
    assert os.path.isfile(processor_c_path), f"Processor source file missing: {processor_c_path}"

def test_processor_executable_exists():
    processor_bin_path = "/home/user/rpc_utility/bin/processor"
    assert os.path.isfile(processor_bin_path), f"Processor executable missing: {processor_bin_path}"
    assert os.access(processor_bin_path, os.X_OK), f"Processor executable is not marked as executable: {processor_bin_path}"

def test_allowed_log_contents():
    log_path = "/home/user/rpc_utility/allowed.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = ["101", "102", "103", "105", "106", "109"]
    assert lines == expected_ids, f"allowed.log contents are incorrect. Expected {expected_ids}, got {lines}"