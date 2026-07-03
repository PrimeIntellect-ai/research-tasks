# test_final_state.py
import os
import pytest

POLYBUILD_DIR = "/home/user/polybuild"

def test_polybuild_directory_exists():
    assert os.path.isdir(POLYBUILD_DIR), f"Directory {POLYBUILD_DIR} does not exist"

def test_source_files_exist():
    proto_file = os.path.join(POLYBUILD_DIR, "catalog.proto")
    c_file = os.path.join(POLYBUILD_DIR, "api_endpoint.c")
    makefile = os.path.join(POLYBUILD_DIR, "Makefile")

    assert os.path.isfile(proto_file), f"{proto_file} does not exist"
    assert os.path.isfile(c_file), f"{c_file} does not exist"
    assert os.path.isfile(makefile), f"{makefile} does not exist"

def test_generated_and_compiled_files_exist():
    pb_c = os.path.join(POLYBUILD_DIR, "catalog.pb-c.c")
    pb_h = os.path.join(POLYBUILD_DIR, "catalog.pb-c.h")
    executable = os.path.join(POLYBUILD_DIR, "api_endpoint")

    assert os.path.isfile(pb_c), f"Generated file {pb_c} does not exist"
    assert os.path.isfile(pb_h), f"Generated file {pb_h} does not exist"
    assert os.path.isfile(executable), f"Executable {executable} does not exist"
    assert os.access(executable, os.X_OK), f"{executable} is not executable"

def test_response_bin_contents():
    response_file = os.path.join(POLYBUILD_DIR, "response.bin")
    assert os.path.isfile(response_file), f"Output file {response_file} does not exist"

    with open(response_file, 'rb') as f:
        data = f.read()

    # Split headers and body
    parts = data.split(b'\r\n\r\n', 1)
    if len(parts) != 2:
        # Fallback in case they used \n\n instead of \r\n\r\n
        parts = data.split(b'\n\n', 1)

    assert len(parts) == 2, "Could not find HTTP header/body separator (CRLF CRLF or LF LF)"
    headers, body = parts

    assert b'Content-Type: application/x-protobuf' in headers, "Missing or incorrect Content-Type header in response.bin"

    # The expected serialized protobuf payload for id=101, slug="mechanical-keyboard", in_stock=true
    expected_body = b'\x08\x65\x12\x13mechanical-keyboard\x18\x01'

    assert body == expected_body, f"Protobuf payload mismatch. Expected {expected_body.hex()}, got {body.hex()}"