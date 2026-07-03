# test_final_state.py

import os
import json
import tarfile
import tempfile
import pytest

def test_report_json_exists_and_correct():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "changed" in report, "Report missing 'changed' key."
    assert "new" in report, "Report missing 'new' key."

    assert sorted(report["changed"]) == ["app/config.json", "system/network.json"], "Incorrect 'changed' files list."
    assert sorted(report["new"]) == ["app/db.json"], "Incorrect 'new' files list."

def test_extracted_directories_no_ini():
    extracted_base = "/home/user/extracted"
    for v in ["v1", "v2", "v3"]:
        v_dir = os.path.join(extracted_base, v)
        if not os.path.isdir(v_dir):
            continue # We test archive contents directly, but if they left it, check it.
        for root, _, files in os.walk(v_dir):
            for file in files:
                assert not file.endswith(".ini"), f"Found .ini file {file} in {v_dir}"

def test_latest_config_archive():
    archive_path = "/home/user/latest_config.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError:
            pytest.fail(f"Archive {archive_path} is not a valid tar.gz file.")

        # Check report.json
        tmp_report = os.path.join(tmpdir, "report.json")
        assert os.path.isfile(tmp_report), "report.json missing from root of latest_config.tar.gz"

        # Check system/network.json
        network_json = os.path.join(tmpdir, "system", "network.json")
        assert os.path.isfile(network_json), "system/network.json missing from archive"
        with open(network_json, 'r') as f:
            net_data = json.load(f)
        assert net_data == {"interface": {"eth0": "static", "mtu": "9000"}}, "system/network.json content is incorrect"

        # Check app/config.json
        app_config = os.path.join(tmpdir, "app", "config.json")
        assert os.path.isfile(app_config), "app/config.json missing from archive"

        # Check app/db.json
        db_json = os.path.join(tmpdir, "app", "db.json")
        assert os.path.isfile(db_json), "app/db.json missing from archive"
        with open(db_json, 'r') as f:
            db_data = json.load(f)
        assert db_data == {"mysql": {"host": "localhost", "port": "3306"}}, "app/db.json content is incorrect"

        # Ensure no .ini files
        for root, _, files in os.walk(tmpdir):
            for file in files:
                assert not file.endswith(".ini"), f"Found .ini file {file} in archive"