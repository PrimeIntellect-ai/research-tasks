# test_final_state.py

import os
import requests
import tempfile
from pathlib import Path

def test_no_broken_symlinks():
    path = Path("/home/user/research_data")
    broken_symlinks = []
    for p in path.rglob("*.log"):
        if p.is_symlink() and not p.exists():
            broken_symlinks.append(p)
    assert len(broken_symlinks) == 0, f"Found broken symlinks that should have been deleted: {broken_symlinks}"

def test_tar_gz_extracted():
    # We assume the extraction produced at least some .log files that were not there before.
    # Since we don't know the exact names, we just ensure that the directory has .log files.
    path = Path("/home/user/research_data")
    log_files = list(path.rglob("*.log"))
    assert len(log_files) > 0, "No .log files found, extraction might have failed or files were deleted."

def test_rust_server_process_endpoint():
    # Create a temporary directory with a controlled log file to test the server
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = Path(tmpdir) / "test_data.log"

        record1 = "This record has no uppercase vowels."
        record2 = "This record has A E I O U and should score eighty-five."
        record3 = "This record has A E I and should score fifty."
        record4 = "Another record with U U U U U to score high."

        with open(log_path, "w") as f:
            f.write(f"{record1}\n---END_RECORD---\n{record2}\n---END_RECORD---\n{record3}\n---END_RECORD---\n{record4}\n")

        try:
            response = requests.post("http://127.0.0.1:9090/process", data=tmpdir, timeout=5)
        except requests.exceptions.RequestException as e:
            assert False, f"Failed to connect to the Rust server on 127.0.0.1:9090 or request failed: {e}"

        assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

        # The expected output is record2 and record4 separated by \n\n
        expected_output = f"{record2}\n\n{record4}\n"

        # Depending on how the student handled trailing newlines in records, we strip for comparison
        actual_records = [r.strip() for r in response.text.split("\n\n") if r.strip()]
        expected_records = [record2, record4]

        assert actual_records == expected_records, f"Server returned incorrect records. Expected: {expected_records}, Got: {actual_records}"