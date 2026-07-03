# test_final_state.py

import os
import tarfile
import tempfile
import requests
import pytest

def test_server_and_archive():
    url = "http://127.0.0.1:8080/clean_projects.tar.gz"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or fetch the archive at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text[:200]}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tar_path = os.path.join(tmpdir, "clean_projects.tar.gz")
        with open(tar_path, "wb") as f:
            f.write(response.content)

        try:
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError as e:
            pytest.fail(f"Failed to extract tarball. The file served might not be a valid gzip-compressed tarball: {e}")

        # Check that .bak files do not exist
        main_c_bak = os.path.join(tmpdir, "src", "main.c.bak")
        old_bak = os.path.join(tmpdir, "config", "old.bak")
        assert not os.path.exists(main_c_bak), "Backup file main.c.bak was not deleted and is present in the archive."
        assert not os.path.exists(old_bak), "Backup file old.bak was not deleted and is present in the archive."

        # Check settings.conf in config/
        config_settings = os.path.join(tmpdir, "config", "settings.conf")
        assert os.path.exists(config_settings), "config/settings.conf is missing from the archive. Ensure internal paths are relative to /home/user/projects/"
        with open(config_settings, "r") as f:
            content = f.read()
            assert "SECRET_TOKEN=REDACTED" in content, "config/settings.conf does not contain SECRET_TOKEN=REDACTED"
            assert "SECRET_TOKEN=abc123xyz" not in content, "config/settings.conf still contains the old secret token (abc123xyz)"

        # Check settings.conf in root
        root_settings = os.path.join(tmpdir, "settings.conf")
        assert os.path.exists(root_settings), "settings.conf is missing from the root of the archive. Ensure internal paths are relative to /home/user/projects/"
        with open(root_settings, "r") as f:
            content = f.read()
            assert "SECRET_TOKEN=REDACTED" in content, "settings.conf does not contain SECRET_TOKEN=REDACTED"
            assert "SECRET_TOKEN=dev_token" not in content, "settings.conf still contains the old secret token (dev_token)"

def test_bash_serve_fixed():
    script_path = "/app/bash-serve/serve.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing"

    with open(script_path, "r") as f:
        content = f.read()
        assert "-Z" not in content, f"The invalid '-Z' flag is still present in {script_path}"