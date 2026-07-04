# test_final_state.py

import os
import tarfile
import json
import tempfile
import pytest

def test_clean_project_archive_exists_and_valid():
    archive_path = "/home/user/clean_project.tar.bz2"
    assert os.path.isfile(archive_path), f"Archive not found: {archive_path}"
    assert tarfile.is_tarfile(archive_path), f"Not a valid tar archive: {archive_path}"

    with tarfile.open(archive_path, "r:bz2") as tar:
        members = tar.getnames()
        assert len(members) > 0, "The clean project archive is empty"

        # Ensure no nested archives
        for member in members:
            assert not member.endswith(".zip"), f"Nested zip archive found: {member}"
            assert not member.endswith(".tar.gz"), f"Nested tar.gz archive found: {member}"

def test_todo_report_json():
    report_path = "/home/user/todo_report.json"
    assert os.path.isfile(report_path), f"JSON report not found: {report_path}"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON")

    expected_report = {
        "core.py": 2,
        "plugin_a.py": 2,
        "plugin_b.py": 4
    }

    assert report == expected_report, f"JSON report content is incorrect. Expected {expected_report}, got {report}"

def test_archive_contents_and_transformations():
    archive_path = "/home/user/clean_project.tar.bz2"
    assert os.path.isfile(archive_path), f"Archive not found: {archive_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, "r:bz2") as tar:
            tar.extractall(path=tmpdir)

        py_files_found = []
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                if file.endswith(".py"):
                    py_files_found.append(file)
                    filepath = os.path.join(root, file)
                    with open(filepath, "r") as f:
                        content = f.read()

                    assert "FIXME:" not in content, f"'FIXME:' found in {file}"

                    if file == "core.py":
                        assert content.count("TODO:") == 2, f"Expected 2 'TODO:' in core.py, found {content.count('TODO:')}"
                    elif file == "plugin_a.py":
                        assert content.count("TODO:") == 2, f"Expected 2 'TODO:' in plugin_a.py, found {content.count('TODO:')}"
                    elif file == "plugin_b.py":
                        assert content.count("TODO:") == 4, f"Expected 4 'TODO:' in plugin_b.py, found {content.count('TODO:')}"

        assert "core.py" in py_files_found, "core.py is missing from the archive"
        assert "plugin_a.py" in py_files_found, "plugin_a.py is missing from the archive"
        assert "plugin_b.py" in py_files_found, "plugin_b.py is missing from the archive"