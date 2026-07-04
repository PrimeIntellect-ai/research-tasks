# test_final_state.py
import os
import tarfile
import subprocess
import shutil
import pytest

def test_curation_accuracy():
    assert os.path.exists("/app/archived.tar"), "Missing /app/archived.tar"
    assert os.path.exists("/app/curated_repo.tar.xz"), "Missing /app/curated_repo.tar.xz"

    correct = 0
    total = 0

    # Check archived.tar
    with tarfile.open("/app/archived.tar", "r") as tar:
        for member in tar.getmembers():
            if member.isfile():
                total += 1
                if member.name.endswith(".bdat"):
                    correct += 1

    # Check curated_repo.tar.xz
    extract_dir = "/tmp/eval_repo_extract"
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    os.makedirs(extract_dir, exist_ok=True)

    try:
        subprocess.run(["tar", "-xf", "/app/curated_repo.tar.xz", "-C", extract_dir], check=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to extract /app/curated_repo.tar.xz")

    for root, dirs, files in os.walk(extract_dir):
        for f in files:
            total += 1
            if "legacy-v1-" not in f and "beta-v2-" not in f and not f.endswith(".bdat"):
                correct += 1
            if f.endswith(".manifest"):
                with open(os.path.join(root, f), "r", errors="ignore") as mf:
                    lines = mf.readlines()
                    total += 1
                    # Check header stripped and text replaced
                    if len(lines) > 0 and "legacy-v1-" not in "".join(lines):
                        correct += 1

    accuracy = correct / total if total > 0 else 0

    shutil.rmtree(extract_dir, ignore_errors=True)

    assert accuracy >= 0.98, f"Curation Accuracy Ratio {accuracy:.4f} is below threshold 0.98"