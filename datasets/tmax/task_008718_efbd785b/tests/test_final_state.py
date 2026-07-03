# test_final_state.py

import os
import tarfile

def test_script_exists():
    assert os.path.isfile("/home/user/sanitize_archive.py"), "/home/user/sanitize_archive.py is missing."

def test_report_file():
    report_path = "/home/user/backups/report.txt"
    assert os.path.isfile(report_path), f"{report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "Removed: 14 lines", f"Expected report.txt to contain 'Removed: 14 lines', but got '{content}'."

def test_sanitized_archive_exists_and_valid():
    archive_path = "/home/user/backups/sanitized_app_logs.tar.gz"
    assert os.path.isfile(archive_path), f"{archive_path} is missing."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getmembers()
            filenames = [m.name for m in members]

            # Check for exactly the 5 log files
            expected_filenames = {f"service_{i}.log" for i in range(1, 6)}
            actual_filenames = set(filenames)

            assert expected_filenames.issubset(actual_filenames), f"Archive is missing some expected log files. Found: {filenames}"

            # Check for leaks
            total_leaks = 0
            for member in members:
                if not member.isfile():
                    continue
                f = tar.extractfile(member)
                if f is not None:
                    lines = f.read().decode('utf-8').splitlines()
                    leaks = sum(1 for line in lines if line.startswith("CREDENTIAL_LEAK:"))
                    total_leaks += leaks

            assert total_leaks == 0, f"Found {total_leaks} CREDENTIAL_LEAK lines in the sanitized archive. It should be 0."

    except tarfile.ReadError:
        assert False, f"Failed to read {archive_path}. It must be a valid gzip-compressed tar archive."