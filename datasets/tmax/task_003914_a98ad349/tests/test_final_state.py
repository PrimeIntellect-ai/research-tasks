# test_final_state.py

import os
import subprocess
import pytest

def test_result_log():
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you run the test script and redirect output?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "SERVER_STARTED_SUCCESSFULLY" in content, "The result.log does not contain the expected success message."

def test_shared_library_exists_and_valid():
    so_path = "/home/user/project/libfastparser.so"
    assert os.path.isfile(so_path), f"{so_path} does not exist. Did you run make?"

    # Check if it's an ELF shared object
    with open(so_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{so_path} is not a valid ELF file."

        # Skip to e_type (offset 16)
        f.seek(16)
        e_type = f.read(2)
        # 0x03 0x00 is ET_DYN (Shared object file) in little endian
        # 0x00 0x03 in big endian
        assert e_type in (b"\x03\x00", b"\x00\x03"), f"{so_path} is not compiled as a shared object. Did you add -shared and -fPIC?"

def test_grpc_files_generated():
    pb2_path = "/home/user/project/service_pb2.py"
    pb2_grpc_path = "/home/user/project/service_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"{pb2_path} does not exist. Did you generate the protobuf files?"
    assert os.path.isfile(pb2_grpc_path), f"{pb2_grpc_path} does not exist. Did you generate the gRPC protobuf files?"