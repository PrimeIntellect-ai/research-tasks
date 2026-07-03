# test_final_state.py
import os
import tarfile
import tempfile

def test_result_log():
    """Test that result.log exists and contains the correct text."""
    result_path = '/home/user/result.log'
    assert os.path.exists(result_path), f"Missing file: {result_path}"
    with open(result_path, 'r') as f:
        content = f.read().strip()
    assert content == "INTEGRITY_VALID", f"Expected 'INTEGRITY_VALID' in {result_path}, got '{content}'"

def test_sanitized_archive():
    """Test that sanitized_data.tar.gz exists, is valid, and contains correctly sanitized files."""
    archive_path = '/home/user/sanitized_data.tar.gz'
    assert os.path.exists(archive_path), f"Missing file: {archive_path}"
    assert tarfile.is_tarfile(archive_path), f"File is not a valid tar archive: {archive_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(path=tmpdir)

        # Find the files
        server_log = None
        database_log = None
        readme_txt = None

        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                if file == "server.log":
                    server_log = os.path.join(root, file)
                elif file == "database.log":
                    database_log = os.path.join(root, file)
                elif file == "readme.txt":
                    readme_txt = os.path.join(root, file)

        assert server_log is not None, "server.log not found in the sanitized archive."
        assert database_log is not None, "database.log not found in the sanitized archive."
        assert readme_txt is not None, "readme.txt not found in the sanitized archive."

        # Check server.log
        with open(server_log, 'r') as f:
            server_content = f.read()
            assert "API_KEY=A1B2C3D4E5" not in server_content, "server.log was not sanitized properly."
            assert "API_KEY=REDACTED" in server_content, "server.log lacks REDACTED string."

        # Check database.log
        with open(database_log, 'r') as f:
            database_content = f.read()
            assert "API_KEY=9988776655QWERTY" not in database_content, "database.log was not sanitized properly."
            assert "API_KEY=REDACTED" in database_content, "database.log lacks REDACTED string."

        # Check readme.txt
        with open(readme_txt, 'r') as f:
            readme_content = f.read()
            assert "API_KEY=EXAMPLEKEY123" in readme_content, "readme.txt was incorrectly modified."
            assert "API_KEY=REDACTED" not in readme_content, "readme.txt should not be sanitized."