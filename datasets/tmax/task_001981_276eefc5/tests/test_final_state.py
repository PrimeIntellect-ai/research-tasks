# test_final_state.py
import tarfile
import os
import pytest

def test_bash_script_exists():
    script_path = "/home/user/run_backup.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."

def test_manifest_exists():
    manifest_path = "/home/user/backup_manifest.csv"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

def test_incremental_tar_gz_f1_score():
    archive_path = "/home/user/incremental.tar.gz"
    assert os.path.isfile(archive_path), f"Archive not found: {archive_path}"

    expected_files = {
        "config_3.yaml",
        "config_12.yaml",
        "config_45.yaml",
        "config_88.yaml",
        "config_91.yaml"
    }

    actual_files = set()
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith(".yaml"):
                    actual_files.add(os.path.basename(member.name))
    except Exception as e:
        pytest.fail(f"Error reading archive {archive_path}: {e}")

    true_positives = len(expected_files.intersection(actual_files))
    false_positives = len(actual_files - expected_files)
    false_negatives = len(expected_files - actual_files)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"Metric F1 Score: {f1:.4f} is below threshold 0.95. Expected: {expected_files}, Actual: {actual_files}"