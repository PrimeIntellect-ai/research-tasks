# test_final_state.py
import os
import tarfile

def test_binary_timestamps_content():
    """Verify that binary_timestamps.txt contains the correctly extracted timestamps."""
    file_path = '/home/user/binary_timestamps.txt'
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ['100', '200']
    assert lines == expected, f"Expected {expected} in {file_path}, but got {lines}"

def test_summary_csv_content():
    """Verify that summary.csv contains the correct error logs sorted by id."""
    file_path = '/home/user/summary.csv'
    assert os.path.isfile(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        'id,status',
        '101,ERROR',
        '105,ERROR',
        '108,ERROR'
    ]
    assert lines == expected, f"Expected {expected} in {file_path}, but got {lines}"

def test_final_report_tar_gz():
    """Verify that final_report.tar.gz exists and contains exactly the required files at the root."""
    archive_path = '/home/user/final_report.tar.gz'
    assert os.path.isfile(archive_path), f"Archive not found: {archive_path}"

    try:
        with tarfile.open(archive_path, 'r:gz') as tar:
            members = tar.getnames()
    except tarfile.ReadError:
        assert False, f"Failed to read {archive_path} as a tar.gz archive"

    expected_members = {'summary.csv', 'binary_timestamps.txt'}
    assert set(members) == expected_members, f"Archive {archive_path} must contain exactly {expected_members} at the root, but got {members}"