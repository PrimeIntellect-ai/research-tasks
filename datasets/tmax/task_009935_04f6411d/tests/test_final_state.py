# test_final_state.py

import os
import tarfile
import pytest

def test_tracker_cpp_exists():
    tracker_cpp = "/home/user/tracker.cpp"
    assert os.path.isfile(tracker_cpp), f"Expected C++ source file {tracker_cpp} is missing."

def test_tarball_exists():
    tarball = "/home/user/remote_archive/sync_data.tar.gz"
    assert os.path.isfile(tarball), f"Expected tarball {tarball} is missing."

def test_tarball_contents():
    tarball_path = "/home/user/remote_archive/sync_data.tar.gz"
    assert os.path.isfile(tarball_path), f"Cannot test contents, {tarball_path} does not exist."

    expected_csv = (
        "Timestamp,KeyA,KeyB\n"
        "2023-11-01T08:00:00Z,MAX_CONNECTIONS,MAX_CONNECTIONS\n"
        "2023-11-01T09:00:00Z,WORKER_THREADS,WORKER_THREADS\n"
        "2023-11-01T10:30:00Z,CACHE_SIZE,LOG_LEVEL"
    )

    found_csv = False
    csv_content = ""

    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            for member in tar.getmembers():
                if member.name.endswith("aligned_features.csv"):
                    found_csv = True
                    f = tar.extractfile(member)
                    if f is not None:
                        csv_content = f.read().decode('utf-8').strip()
                    break
    except tarfile.TarError as e:
        pytest.fail(f"Failed to open or read tarball {tarball_path}: {e}")

    assert found_csv, "aligned_features.csv was not found inside the tarball."

    # Normalize line endings for comparison
    normalized_actual = "\n".join([line.strip() for line in csv_content.splitlines() if line.strip()])
    normalized_expected = "\n".join([line.strip() for line in expected_csv.splitlines() if line.strip()])

    assert normalized_actual == normalized_expected, (
        "The contents of aligned_features.csv inside the tarball do not match the expected output.\n"
        f"Expected:\n{normalized_expected}\n\nActual:\n{normalized_actual}"
    )