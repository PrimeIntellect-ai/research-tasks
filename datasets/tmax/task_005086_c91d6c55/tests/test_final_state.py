# test_final_state.py

import os
import tarfile
import pytest

def test_artifact_report():
    report_path = '/home/user/artifact_report.txt'
    expected_path = '/home/user/.expected_report.txt'

    assert os.path.exists(report_path), f"The report file {report_path} is missing."

    with open(report_path, 'r') as f:
        actual_report = f.read()

    with open(expected_path, 'r') as f:
        expected_report = f.read()

    assert actual_report == expected_report, "The contents of artifact_report.txt do not match the expected output."

def test_curated_binaries_archive():
    archive_path = '/home/user/curated_binaries.tar.gz'
    expected_path = '/home/user/.expected_report.txt'

    assert os.path.exists(archive_path), f"The archive {archive_path} is missing."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    # Get expected elf filenames from the report
    with open(expected_path, 'r') as f:
        lines = f.read().strip().split('\n')
        expected_elf_files = set()
        for line in lines:
            if line.strip():
                parts = line.split('  ')
                if len(parts) == 2:
                    expected_elf_files.add(parts[1].strip())

    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            members = tar.getmembers()

            # Check for no directories
            for member in members:
                assert not member.isdir(), f"Archive contains a directory '{member.name}', but it should only contain files at the root."
                assert os.path.dirname(member.name) == '', f"File '{member.name}' is not at the root of the archive."

            actual_files = set([m.name for m in members])
            assert actual_files == expected_elf_files, f"The archive contents {actual_files} do not exactly match the expected ELF files {expected_elf_files}."

    except tarfile.TarError as e:
        pytest.fail(f"Failed to read {archive_path}: {e}")

def test_extracted_repo_state():
    repo_dir = '/home/user/extracted_repo'
    assert os.path.exists(repo_dir), f"The directory {repo_dir} is missing."
    assert os.path.isdir(repo_dir), f"{repo_dir} is not a directory."

    items = os.listdir(repo_dir)

    elf_count = 0
    png_count = 0
    pdf_count = 0

    for item in items:
        item_path = os.path.join(repo_dir, item)

        # Check that there are no symlinks
        assert not os.path.islink(item_path), f"Found a symlink '{item}' in {repo_dir}, but all symlinks should have been deleted."

        if os.path.isfile(item_path):
            if item.endswith('.elf'):
                elf_count += 1
            elif item.endswith('.png'):
                png_count += 1
            elif item.endswith('.pdf'):
                pdf_count += 1
            else:
                pytest.fail(f"File '{item}' does not have a valid extension (.elf, .png, .pdf) or was not expected.")

    assert elf_count == 5, f"Expected 5 .elf files in {repo_dir}, found {elf_count}."
    assert png_count == 3, f"Expected 3 .png files in {repo_dir}, found {png_count}."
    assert pdf_count == 4, f"Expected 4 .pdf files in {repo_dir}, found {pdf_count}."