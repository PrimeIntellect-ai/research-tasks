# test_final_state.py

import os
import glob
import tarfile
import pytest

DATA_DIR = "/home/user/data"
ARCHIVE_PATH = "/home/user/dataset_backup.tar.gz"

EXPECTED_CSVS = {
    "dataset_A.csv": "id,val\n1,100\n2,150",
    "dataset_B.csv": "id,val\n3,200\n4,250",
    "dataset_C.csv": "id,val\n5,300",
}

def normalize_csv_content(content: str) -> str:
    lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    return "\n".join(lines)

def test_csv_files_exist_and_content_correct():
    for filename, expected_content in EXPECTED_CSVS.items():
        filepath = os.path.join(DATA_DIR, filename)
        assert os.path.isfile(filepath), f"Expected CSV file {filepath} is missing."

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        assert normalize_csv_content(content) == normalize_csv_content(expected_content), \
            f"Content of {filepath} does not match the expected CSV data."

def test_no_json_files_remain():
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    assert len(json_files) == 0, f"JSON files were not deleted: {json_files}"

def test_archive_exists_and_contents():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive {ARCHIVE_PATH} is missing."

    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        members = tar.getnames()

        # Check that the expected files are in the archive
        expected_archive_files = [f"data/{name}" for name in EXPECTED_CSVS.keys()]

        for expected_file in expected_archive_files:
            assert expected_file in members, f"File {expected_file} is missing from the archive."

        # Verify content inside the archive
        for filename, expected_content in EXPECTED_CSVS.items():
            member_name = f"data/{filename}"
            member = tar.getmember(member_name)
            assert member.isfile(), f"Archive member {member_name} is not a file."

            f = tar.extractfile(member)
            assert f is not None, f"Could not extract {member_name} from archive."

            content = f.read().decode("utf-8")
            assert normalize_csv_content(content) == normalize_csv_content(expected_content), \
                f"Content of {member_name} inside archive does not match expected data."