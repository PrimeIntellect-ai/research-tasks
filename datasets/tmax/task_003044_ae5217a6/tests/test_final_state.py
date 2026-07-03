# test_final_state.py
import os
import tarfile

EXPECTED_FILES = [
    "app1_chunk_aa.txt",
    "app1_chunk_ab.txt",
    "app1_chunk_ac.txt",
    "app2_chunk_aa.txt",
    "db_sync_chunk_aa.txt",
    "db_sync_chunk_ab.txt",
    "db_sync_chunk_ac.txt",
    "db_sync_chunk_ad.txt",
    "db_sync_chunk_ae.txt"
]

def test_process_logs_script():
    script_path = "/home/user/process_logs.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

    with open(script_path, "r") as f:
        content = f.read()

    assert "flock" in content, "The script must use 'flock' to obtain a file lock."

def test_report_txt():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == EXPECTED_FILES, f"Contents of {report_path} do not match the expected list of files."

def test_final_chunks_archive():
    archive_path = "/home/user/final_chunks.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getnames()

    members_sorted = sorted(members)
    assert members_sorted == EXPECTED_FILES, (
        f"Contents of {archive_path} do not match the expected flat structure. "
        f"Expected {EXPECTED_FILES}, but got {members_sorted}."
    )