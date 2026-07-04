# test_final_state.py
import os
import json
import tarfile
import csv
from pathlib import Path

def test_csv_report():
    report_path = Path("/home/user/archive_report.csv")
    assert report_path.exists(), f"Report file {report_path} is missing."
    assert report_path.is_file(), f"Report {report_path} must be a regular file."

    with open(report_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV report is empty."
    assert rows[0] == ["filepath", "new_status"], f"CSV header mismatch. Got: {rows[0]}"

    data_rows = rows[1:]
    expected_rows = [
        ["dir D/file 5.json", "archived"],
        ["dir_A/file1.json", "archived"]
    ]

    assert data_rows == expected_rows, (
        f"CSV data rows mismatch or not sorted correctly.\n"
        f"Expected: {expected_rows}\n"
        f"Got:      {data_rows}"
    )

def test_tarball_archive():
    tar_path = Path("/home/user/cold_storage.tar.gz")
    assert tar_path.exists(), f"Archive {tar_path} is missing."
    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar archive."

    expected_files = {
        "dir D/file 5.json",
        "dir_A/file1.json"
    }

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getmembers()
        # Filter out directories if any were added
        file_members = [m for m in members if m.isfile()]
        archived_paths = {m.name for m in file_members}

        # Normalize paths (e.g., remove leading './' if present)
        normalized_paths = {p.lstrip("./") for p in archived_paths}

        assert normalized_paths == expected_files, (
            f"Tarball contents mismatch.\n"
            f"Expected: {expected_files}\n"
            f"Got:      {normalized_paths}"
        )

        for member in file_members:
            norm_name = member.name.lstrip("./")
            if norm_name in expected_files:
                f = tar.extractfile(member)
                assert f is not None, f"Could not read {member.name} from archive."
                content = f.read().decode("utf-8")
                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    assert False, f"Archived file {member.name} is not valid JSON."

                assert data.get("status") == "archived", (
                    f"Archived file {member.name} does not have status 'archived'. "
                    f"Got: {data.get('status')}"
                )

def test_active_volume_cleanup():
    data_volume = Path("/home/user/data_volume")

    # Files that should have been deleted
    deleted_files = [
        "dir_A/file1.json",
        "dir D/file 5.json"
    ]
    for rel_path in deleted_files:
        file_path = data_volume / rel_path
        assert not file_path.exists(), f"File {file_path} should have been deleted from active volume."

    # Files that should remain untouched
    untouched_files = {
        "dir_A/file2.json": {"id": 2, "status": "archivable", "data": "content B"},
        "dir_B/sub_C/file3.json": {"id": 3, "status": "archivable", "data": "content C"},
        "dir_B/sub_C/file4.json": {"id": 4, "status": "active", "data": "content D"}
    }

    for rel_path, expected_content in untouched_files.items():
        file_path = data_volume / rel_path
        assert file_path.exists(), f"File {file_path} should not have been deleted."

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                assert False, f"File {file_path} is no longer valid JSON."

            assert data == expected_content, (
                f"Content of {file_path} was modified.\n"
                f"Expected: {expected_content}\n"
                f"Got:      {data}"
            )