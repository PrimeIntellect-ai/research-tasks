# test_final_state.py

import os
import urllib.request
import urllib.error

def test_nginx_proxy_returns_hello_world():
    """Test that Nginx is running, proxying to the Python app, and returning 'Hello World'."""
    try:
        req = urllib.request.Request("http://localhost:8080")
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            assert content == "Hello World\n", f"Expected 'Hello World\\n' but got '{content}'"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to http://localhost:8080: {e}. Is Nginx and the Python app running?"

def test_backup_script_exists():
    """Test that the backup script was created."""
    assert os.path.isfile("/home/user/backup.py"), "Backup script /home/user/backup.py does not exist."

def test_backup_file_exists_and_content():
    """Test that the backup file exists, has the fixed proxy_pass, and ends with the correct string."""
    backup_file = "/home/user/backup/nginx.conf.bak"
    assert os.path.isfile(backup_file), f"Backup file {backup_file} does not exist."

    with open(backup_file, "r") as f:
        content = f.read()
        lines = content.splitlines()

    assert "proxy_pass http://unix:/home/user/app/app.sock;" in content, \
        "The backup file does not contain the fixed proxy_pass directive."

    assert len(lines) > 0, "The backup file is empty."
    assert lines[-1] == "# BACKUP SUCCESSFUL", \
        f"The last line of the backup file must be exactly '# BACKUP SUCCESSFUL', but got '{lines[-1]}'."