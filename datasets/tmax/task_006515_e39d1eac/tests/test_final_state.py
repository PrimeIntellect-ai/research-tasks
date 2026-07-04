# test_final_state.py
import os
import hashlib

def test_final_state():
    curated_dir = "/home/user/curated"

    file1 = os.path.join(curated_dir, "x86_64", "app", "app-x86_64-v1.tar.gz")
    file2 = os.path.join(curated_dir, "arm64", "app", "app-arm64-v1.zip")

    assert os.path.isfile(file1), f"Expected curated file not found: {file1}"
    assert os.path.isfile(file2), f"Expected curated file not found: {file2}"

    def get_sha256(filepath):
        hash_sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    hash1 = get_sha256(file1)
    hash2 = get_sha256(file2)

    csv_path = os.path.join(curated_dir, "verified_manifest.csv")
    assert os.path.isfile(csv_path), f"CSV manifest not found: {csv_path}"

    with open(csv_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 3, f"Expected 3 lines in CSV (header + 2 rows), got {len(lines)}"
    assert lines[0] == "filename,architecture,project,sha256", f"CSV header incorrect: {lines[0]}"

    expected_row1 = f"app-arm64-v1.zip,arm64,app,{hash2}"
    expected_row2 = f"app-x86_64-v1.tar.gz,x86_64,app,{hash1}"

    assert lines[1] == expected_row1, f"CSV row 1 incorrect. Expected '{expected_row1}', got '{lines[1]}'"
    assert lines[2] == expected_row2, f"CSV row 2 incorrect. Expected '{expected_row2}', got '{lines[2]}'"

    # Check that corrupt/bitrot files were excluded from the curated directory
    for root, dirs, files in os.walk(curated_dir):
        assert "lib-x86_64-v2.tar.gz" not in files, "Corrupted archive 'lib-x86_64-v2.tar.gz' was incorrectly moved to curated directory"
        assert "tools-arm64-v3.tar.gz" not in files, "Bit-rot archive 'tools-arm64-v3.tar.gz' was incorrectly moved to curated directory"