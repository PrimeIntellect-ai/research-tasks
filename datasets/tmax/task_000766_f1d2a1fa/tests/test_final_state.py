# test_final_state.py

import os
import difflib
import tarfile
import time

def test_recovered_artifact_metric():
    expected_path = "/app/.hidden/expected_artifact.tar.gz"
    recovered_path = "/home/user/recovered_artifact.tar.gz"

    assert os.path.exists(recovered_path), f"Recovered artifact not found at {recovered_path}"

    with open(expected_path, 'rb') as f:
        expected = f.read()
    with open(recovered_path, 'rb') as f:
        recovered = f.read()

    sm = difflib.SequenceMatcher(None, expected, recovered)
    ratio = sm.ratio()
    assert ratio >= 0.98, f"Recovered artifact ratio {ratio} is below threshold 0.98"

def test_legacy_binaries_extracted():
    expected_path = "/app/.hidden/expected_artifact.tar.gz"
    legacy_txt_path = "/home/user/legacy_binaries.txt"
    repo_path = "/home/user/repo"

    assert os.path.isdir(repo_path), f"Extracted repo directory not found at {repo_path}"
    assert os.path.exists(legacy_txt_path), f"Legacy binaries file not found at {legacy_txt_path}"

    # Re-derive expected legacy binaries from the hidden expected artifact
    expected_files = []
    with tarfile.open(expected_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile():
                # >10KB (10240 bytes) and created before 2023
                if member.size > 10240 and member.mtime < time.mktime(time.strptime("2023-01-01", "%Y-%m-%d")):
                    expected_files.append(os.path.basename(member.name))

    expected_files.sort()

    with open(legacy_txt_path, "r") as f:
        actual_content = f.read().strip()

    actual_files = [line.strip() for line in actual_content.splitlines() if line.strip()]
    actual_basenames = sorted([os.path.basename(f) for f in actual_files])

    assert actual_basenames == expected_files, f"Expected legacy binaries {expected_files}, but got {actual_basenames} in {legacy_txt_path}"