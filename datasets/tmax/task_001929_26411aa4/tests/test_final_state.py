# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_extractor_source_exists():
    source_path = "/home/user/extractor.c"
    assert os.path.isfile(source_path), f"Source file {source_path} does not exist"

    with open(source_path, "r") as f:
        content = f.read()

    # Check if <elf.h> is included as required by the prompt
    assert "<elf.h>" in content, "The C program must use the ELF format specification and include <elf.h>"

def test_extractor_binary_exists():
    binary_path = "/home/user/extractor"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist"
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable"

def test_final_archive_exists_and_correct():
    archive_path = "/home/user/final_archive.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist"

    expected_csv_content = (
        "trial,outcome,time\n"
        "012,partial,162310\n"
        "042,failure,162345\n"
        "089,success,162399\n"
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError as e:
            pytest.fail(f"Failed to extract tarball {archive_path}: {e}")

        # The prompt says compress the summary.csv file. It might be extracted as summary.csv or home/user/summary.csv
        # Let's search for summary.csv in the extracted files
        extracted_csv_path = None
        for root, dirs, files in os.walk(tmpdir):
            if "summary.csv" in files:
                extracted_csv_path = os.path.join(root, "summary.csv")
                break

        assert extracted_csv_path is not None, "summary.csv was not found inside the final_archive.tar.gz"

        with open(extracted_csv_path, "r") as f:
            actual_content = f.read().strip()

        expected_content_stripped = expected_csv_content.strip()

        assert actual_content == expected_content_stripped, (
            f"Contents of summary.csv do not match the expected output.\n"
            f"Expected:\n{expected_content_stripped}\n\n"
            f"Actual:\n{actual_content}"
        )