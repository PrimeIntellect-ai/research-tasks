# test_final_state.py
import os
import tarfile
import pytest

def test_extraction_log():
    log_path = '/home/user/workspace/extraction.log'
    assert os.path.isfile(log_path), f"Log file missing at {log_path}"

    with open(log_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Original: src/Main-File.txt -> Sanitized: main_file.txt",
        "Original: ../outside-file.txt -> Sanitized: outside_file.txt",
        "Original: deep/dir/../../../secret-Data.txt -> Sanitized: secret_data.txt"
    ]

    assert lines == expected_lines, f"Extraction log content is incorrect. Got: {lines}"

def test_safe_project_tar_gz():
    tar_path = '/home/user/workspace/safe_project.tar.gz'
    assert os.path.isfile(tar_path), f"Tarball missing at {tar_path}"

    expected_files = {
        "main_file.txt": "Café".encode('utf-8'),
        "outside_file.txt": "Hello World".encode('utf-8'),
        "secret_data.txt": "Secret information here.".encode('utf-8')
    }

    try:
        with tarfile.open(tar_path, 'r:gz') as tar:
            members = tar.getmembers()

            extracted_names = [m.name for m in members]

            for expected_name in expected_files.keys():
                assert expected_name in extracted_names, f"Missing {expected_name} in tarball"

            for m in members:
                assert m.isfile(), f"Tarball contains a non-file entry (directories are not allowed): {m.name}"
                assert m.name in expected_files, f"Unexpected file in tarball: {m.name}"

                f = tar.extractfile(m)
                assert f is not None, f"Could not extract file {m.name}"
                content = f.read()

                assert content == expected_files[m.name], f"Content mismatch for {m.name}. Expected {expected_files[m.name]}, got {content}"
    except tarfile.ReadError:
        pytest.fail(f"Could not read {tar_path} as a gzip-compressed tarball")