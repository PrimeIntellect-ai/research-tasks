# test_final_state.py
import os
import json

def test_artifacts_csv_extracted():
    path = "/home/user/output/artifacts.csv"
    assert os.path.isfile(path), f"Expected extracted file {path} does not exist."
    with open(path, "rb") as f:
        content = f.read()
    expected = b"id,artifact_name,checksum\n1,kernel_mod,a1b2c3d4\n2,libssl_custom,f9e8d7c6\n"
    assert content == expected, f"{path} content does not match the expected decompressed payload."

def test_binary_bin_extracted():
    path = "/home/user/output/binary.bin"
    assert os.path.isfile(path), f"Expected extracted file {path} does not exist."
    with open(path, "rb") as f:
        content = f.read()
    expected = b"\x00\x00\x00\x00\xFF\xFF\xFF\xFF" * 10
    assert content == expected, f"{path} content does not match the expected decompressed payload."

def test_malicious_file_not_extracted():
    path = "/home/user/secret_overwrite.txt"
    assert os.path.isfile(path), f"{path} is missing, it should have been left intact."
    with open(path, "r") as f:
        content = f.read()
    assert content == "SAFE", f"Directory traversal attack succeeded! {path} was overwritten."

def test_summary_json_content():
    path = "/home/user/output/summary.json"
    assert os.path.isfile(path), f"JSON output file {path} does not exist."

    with open(path, "r") as f:
        raw_content = f.read()

    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        assert False, f"{path} does not contain valid JSON."

    expected_parsed = [
        {
            "id": "1",
            "artifact_name": "kernel_mod",
            "checksum": "a1b2c3d4"
        },
        {
            "id": "2",
            "artifact_name": "libssl_custom",
            "checksum": "f9e8d7c6"
        }
    ]

    assert parsed == expected_parsed, f"The parsed JSON in {path} does not match the expected structure and values."

    expected_exact = '[\n  {\n    "id": "1",\n    "artifact_name": "kernel_mod",\n    "checksum": "a1b2c3d4"\n  },\n  {\n    "id": "2",\n    "artifact_name": "libssl_custom",\n    "checksum": "f9e8d7c6"\n  }\n]'
    assert raw_content.strip() == expected_exact.strip(), f"The JSON in {path} is correct but does not match the exact expected whitespace/formatting."