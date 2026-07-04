# test_final_state.py

import os
import tarfile
import json
import tempfile
import pytest

def test_converter_c_exists():
    path = "/home/user/converter.c"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    assert "#include" in content, f"{path} does not seem to contain C code (#include missing)."

def test_modern_configs_archive():
    archive_path = "/home/user/modern_configs.tar.gz"
    assert os.path.isfile(archive_path), f"The archive {archive_path} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except Exception as e:
            pytest.fail(f"Failed to extract {archive_path}: {e}")

        # Find the json files
        app1_path = None
        app2_path = None
        for root, _, files in os.walk(tmpdir):
            if "app1.json" in files:
                app1_path = os.path.join(root, "app1.json")
            if "app2.json" in files:
                app2_path = os.path.join(root, "app2.json")

        assert app1_path is not None, "app1.json is missing from the modern_configs.tar.gz archive."
        assert app2_path is not None, "app2.json is missing from the modern_configs.tar.gz archive."

        # Parse and validate app1.json
        try:
            with open(app1_path, "r", encoding="utf-8") as f:
                app1_data = json.load(f)
        except Exception as e:
            pytest.fail(f"Failed to parse app1.json as JSON: {e}")

        assert app1_data.get("General", {}).get("Name") == "Café", "app1.json: General.Name is incorrect."
        assert app1_data.get("General", {}).get("Location") == "Montréal", "app1.json: General.Location is incorrect."
        assert app1_data.get("Network", {}).get("Host") == "españa.local", "app1.json: Network.Host is incorrect."

        # Parse and validate app2.json
        try:
            with open(app2_path, "r", encoding="utf-8") as f:
                app2_data = json.load(f)
        except Exception as e:
            pytest.fail(f"Failed to parse app2.json as JSON: {e}")

        assert app2_data.get("Users", {}).get("Admin") == "François", "app2.json: Users.Admin is incorrect."
        assert app2_data.get("Users", {}).get("Guest") == "Jürgen", "app2.json: Users.Guest is incorrect."
        assert app2_data.get("Access", {}).get("Role") == "Naïve", "app2.json: Access.Role is incorrect."