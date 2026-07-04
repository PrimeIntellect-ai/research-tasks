# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

def test_indexer_sink_score():
    """
    Query the Indexer Sink metrics endpoint and assert that the score
    (received_lines / expected_lines) meets the threshold of 0.95.
    """
    url = "http://localhost:9001/score"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Indexer Sink metrics endpoint at {url}: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON response from {url}: {e}")

    assert "score" in data, f"Response from {url} missing 'score' key. Got: {data}"

    score = float(data["score"])
    threshold = 0.95

    assert score >= threshold, f"Score {score:.4f} is below the required threshold of {threshold}. Data: {data}"

def test_processed_docs_directory_and_manifest():
    """
    Verify that the processed_docs directory exists and contains the manifest file.
    """
    processed_dir = "/home/user/processed_docs"
    manifest_path = os.path.join(processed_dir, "manifest.txt")

    assert os.path.isdir(processed_dir), f"Directory missing: {processed_dir}"
    assert os.path.isfile(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, "Manifest file is empty. It should contain checksums and filenames."
    for line in lines:
        parts = line.strip().split()
        assert len(parts) >= 2, f"Invalid manifest line format: {line.strip()}"

        # The line format should be [SHA256] [filename]
        checksum = parts[0]
        filename = parts[1]

        assert len(checksum) == 64, f"Invalid SHA256 checksum length in manifest: {checksum}"
        assert filename.startswith("chunk_") and filename.endswith(".md"), f"Invalid chunk filename in manifest: {filename}"

        chunk_path = os.path.join(processed_dir, filename)
        assert os.path.isfile(chunk_path), f"Chunk file listed in manifest is missing: {chunk_path}"