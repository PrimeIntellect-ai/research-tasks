# test_final_state.py
import json
import os
import hashlib
import gzip

def test_manifest_exists_and_valid():
    manifest_path = "/home/user/repo_out/manifest.json"
    assert os.path.exists(manifest_path), f"Manifest file not found at {manifest_path}"
    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            assert False, "manifest.json is not valid JSON"

    assert "artifacts" in manifest, "'artifacts' key missing in manifest.json"
    artifacts = manifest["artifacts"]
    assert "lib_core.so" in artifacts, "'lib_core.so' missing in artifacts"
    assert "config.dat" in artifacts, "'config.dat' missing in artifacts"

def test_manifest_sha256_matches_files():
    manifest_path = "/home/user/repo_out/manifest.json"
    assert os.path.exists(manifest_path), "Manifest file is missing"

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    assert "artifacts" in manifest, "'artifacts' key missing in manifest.json"

    for art_name, chunks in manifest["artifacts"].items():
        assert isinstance(chunks, list), f"Expected list of chunks for {art_name}"
        for chunk_info in chunks:
            chunk_filename = chunk_info.get("chunk")
            expected_sha256 = chunk_info.get("sha256")

            assert chunk_filename, f"Missing 'chunk' key in manifest for {art_name}"
            assert expected_sha256, f"Missing 'sha256' key in manifest for {art_name}"

            filepath = os.path.join("/home/user/repo_out", art_name, chunk_filename)
            assert os.path.exists(filepath), f"Chunk file {filepath} does not exist"

            with open(filepath, "rb") as f2:
                actual_sha256 = hashlib.sha256(f2.read()).hexdigest()

            assert actual_sha256 == expected_sha256, f"SHA256 mismatch for {filepath}. Expected {expected_sha256}, got {actual_sha256}"

def test_uncompressed_payloads():
    def verify_payload(art_name, expected_data):
        data = b""
        chunk_idx = 0
        while True:
            filepath = f"/home/user/repo_out/{art_name}/chunk_{chunk_idx}.gz"
            if not os.path.exists(filepath):
                break
            with gzip.open(filepath, "rb") as f:
                data += f.read()
            chunk_idx += 1

        assert chunk_idx > 0, f"No chunks found for {art_name}"
        assert len(data) == len(expected_data), f"Uncompressed data length for {art_name} is {len(data)}, expected {len(expected_data)}"
        assert data == expected_data, f"Uncompressed data for {art_name} does not match expected payload"

    payload1 = bytes([i % 256 for i in range(2500)])
    verify_payload("lib_core.so", payload1)

    payload2 = bytes([(i * 2) % 256 for i in range(1024)])
    verify_payload("config.dat", payload2)