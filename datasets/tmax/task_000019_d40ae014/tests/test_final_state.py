# test_final_state.py
import os
import tarfile
import tempfile
import json
import pytest

ARCHIVE_PATH = "/home/user/final_archive.tar.gz"

def test_archive_exists_and_valid():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive {ARCHIVE_PATH} does not exist."
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"File {ARCHIVE_PATH} is not a valid tar archive."

def test_archive_contents():
    assert os.path.isfile(ARCHIVE_PATH), "Archive missing, cannot check contents."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        # Check logs
        syslog_path = os.path.join(tmpdir, "processed_data", "logs", "systemlog_a1.log")
        applog_path = os.path.join(tmpdir, "processed_data", "logs", "applog_b2.log")

        assert os.path.isfile(syslog_path), "Missing processed_data/logs/systemlog_a1.log in archive."
        assert os.path.isfile(applog_path), "Missing processed_data/logs/applog_b2.log in archive."

        # Check encoding and content
        with open(syslog_path, "rb") as f:
            content = f.read()
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                pytest.fail("systemlog_a1.log is not valid UTF-8.")
            assert "Warning: Memory high" in text, "Content mismatch in systemlog_a1.log"

        with open(applog_path, "rb") as f:
            content = f.read()
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                pytest.fail("applog_b2.log is not valid UTF-8.")
            assert "Error: Disk space low" in text, "Content mismatch in applog_b2.log"

        # Check JSON metrics
        server_json_path = os.path.join(tmpdir, "processed_data", "metrics", "serverstats_jan.json")
        network_json_path = os.path.join(tmpdir, "processed_data", "metrics", "networkstats_jan.json")

        assert os.path.isfile(server_json_path), "Missing processed_data/metrics/serverstats_jan.json in archive."
        assert os.path.isfile(network_json_path), "Missing processed_data/metrics/networkstats_jan.json in archive."

        with open(server_json_path, "r", encoding="utf-8") as f:
            try:
                server_data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail("serverstats_jan.json is not valid JSON.")
            assert isinstance(server_data, list), "serverstats_jan.json should contain an array of objects."
            assert len(server_data) == 2, "serverstats_jan.json should have 2 entries."
            assert str(server_data[0].get("cpu")) == "80", "Incorrect data in serverstats_jan.json."
            assert str(server_data[1].get("disk")) == "80", "Incorrect data in serverstats_jan.json."

        with open(network_json_path, "r", encoding="utf-8") as f:
            try:
                network_data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail("networkstats_jan.json is not valid JSON.")
            assert isinstance(network_data, list), "networkstats_jan.json should contain an array of objects."
            assert len(network_data) == 2, "networkstats_jan.json should have 2 entries."
            assert str(network_data[0].get("rx")) == "1000", "Incorrect data in networkstats_jan.json."
            assert str(network_data[1].get("errors")) == "0", "Incorrect data in networkstats_jan.json."