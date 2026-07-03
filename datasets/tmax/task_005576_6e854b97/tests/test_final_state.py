# test_final_state.py
import os
import tarfile
import tempfile
import glob

def test_changelog_content():
    changelog_path = "/home/user/changelog.txt"
    assert os.path.exists(changelog_path), f"Changelog file missing at {changelog_path}"

    expected_content = (
        "Modified files:\n"
        "server_alpha/app.conf\n"
        "server_alpha/legacy.conf\n"
        "server_beta/cache.conf\n"
        "server_beta/db.conf\n"
        "Total modified: 4\n"
    )

    with open(changelog_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Changelog content does not match expected output.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_normalized_archive_exists_and_structure():
    archive_path = "/home/user/normalized_configs.tar.gz"
    assert os.path.exists(archive_path), f"Normalized archive missing at {archive_path}"
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar.gz file"

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()

        expected_files = [
            "server_alpha/app.conf",
            "server_alpha/system.conf",
            "server_alpha/legacy.conf",
            "server_beta/db.conf",
            "server_beta/cache.conf",
            "server_gamma/web.conf"
        ]

        for expected in expected_files:
            assert expected in names, f"Expected file {expected} not found at root of {archive_path}"

        # Ensure no intermediate "extracted" dir
        for name in names:
            assert not name.startswith("extracted/"), f"Archive incorrectly contains 'extracted/' prefix: {name}"

def test_normalized_archive_contents():
    archive_path = "/home/user/normalized_configs.tar.gz"
    assert os.path.exists(archive_path), f"Normalized archive missing at {archive_path}"

    expected_contents = {
        "server_alpha/app.conf": "ServerName alpha\nPort 443\nLogLevel warn\n# Valid comment\n",
        "server_alpha/system.conf": "OS Linux\nMemory 16G\n",
        "server_alpha/legacy.conf": "OldSetting 1\nPort 443\n",
        "server_beta/db.conf": "DBName beta\nPort 443\nLogLevel info\n",
        "server_beta/cache.conf": "CacheSize 1G\nLogLevel warn\n",
        "server_gamma/web.conf": "Worker 4\nPort 80\nLogLevel warn\n"
    }

    with tarfile.open(archive_path, "r:gz") as tar:
        for fname, expected_text in expected_contents.items():
            try:
                f = tar.extractfile(fname)
                content = f.read().decode("utf-8")
                assert content == expected_text, f"Content mismatch in {fname}.\nExpected:\n{expected_text}\nGot:\n{content}"
            except KeyError:
                assert False, f"File {fname} missing from archive"

def test_script_exists():
    possible_scripts = glob.glob("/home/user/normalize.*")
    valid_extensions = {".py", ".sh", ".rb", ".pl"}

    found = False
    for script in possible_scripts:
        ext = os.path.splitext(script)[1]
        if ext in valid_extensions:
            found = True
            break

    assert found, "Could not find normalize script (e.g., normalize.py, normalize.sh) in /home/user/"