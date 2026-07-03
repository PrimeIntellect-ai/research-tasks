# test_final_state.py

import os
import pytest

WORKDIR = "/home/user/polyglot_test"

def test_libsorter_so_exists():
    so_path = os.path.join(WORKDIR, "libsorter.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} was not found."

def test_protobuf_bindings_exist():
    pb2_path = os.path.join(WORKDIR, "data_pb2.py")
    assert os.path.isfile(pb2_path), f"Protobuf bindings {pb2_path} were not found."

def test_sorted_payloads_txt():
    txt_path = os.path.join(WORKDIR, "sorted_payloads.txt")
    assert os.path.isfile(txt_path), f"Output file {txt_path} was not found."

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Apple",
        "Banana",
        "Cherry",
        "Mango",
        "Xylophone",
        "Zebra"
    ]

    assert lines == expected_lines, f"Contents of {txt_path} do not match the expected sorted decoded strings."

def test_output_bin():
    bin_path = os.path.join(WORKDIR, "output.bin")
    assert os.path.isfile(bin_path), f"Output file {bin_path} was not found."

    with open(bin_path, "rb") as f:
        content = f.read()

    # The expected binary is a protobuf RecordList with the base64 encoded sorted strings.
    # Field 1 (payloads), wire type 2 (length-delimited) -> tag is 0x0A
    expected_content = (
        b'\x0a\x08QXBwbGU='
        b'\x0a\x08QmFuYW5h'
        b'\x0a\x08Q2hlcnJ5'
        b'\x0a\x08TWFuZ28='
        b'\x0a\x0cWHlsb3Bob25l'
        b'\x0a\x08WmVicmE='
    )

    assert content == expected_content, f"Contents of {bin_path} do not match the expected serialized protobuf message."