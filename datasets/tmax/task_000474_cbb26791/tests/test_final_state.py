# test_final_state.py

import os
import pytest

def test_proto_file_exists_and_content():
    proto_path = "/home/user/proto/artifact.proto"
    assert os.path.isfile(proto_path), f"Protobuf file {proto_path} is missing."
    with open(proto_path, "r") as f:
        content = f.read()

    assert "package artifact;" in content, "Proto file is missing 'package artifact;'"
    assert "service ArtifactSigner" in content, "Proto file is missing 'service ArtifactSigner'"
    assert "SignRequest" in content, "Proto file is missing 'SignRequest'"
    assert "SignResponse" in content, "Proto file is missing 'SignResponse'"

def test_rust_library_compiled():
    so_path = "/home/user/rust_lib/target/release/librust_lib.so"
    assert os.path.isfile(so_path), f"Compiled Rust library {so_path} is missing. Did you fix the bug and build in release mode?"

def test_server_script_exists():
    server_path = "/home/user/server/server.py"
    assert os.path.isfile(server_path), f"Server script {server_path} is missing."

def test_client_script_exists():
    client_path = "/home/user/client.py"
    assert os.path.isfile(client_path), f"Client script {client_path} is missing."

def test_final_signature():
    sig_path = "/home/user/final_signature.txt"
    assert os.path.isfile(sig_path), f"Final signature file {sig_path} is missing. Did you run the client?"

    with open(sig_path, "r") as f:
        content = f.read().strip()

    # Base signature calculation:
    # sig = 0
    # for b in b"artifact_v1_release":
    #     sig = (sig * 31 + b) % 1000000007
    # Base is 305886295
    # process_signature: (305886295 ^ 0xDEADBEEF) % 9999991 = 6430342

    expected_sig = "6430342"
    assert content == expected_sig, f"Final signature in {sig_path} is incorrect. Expected {expected_sig}, got {content}."