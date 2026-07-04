# test_final_state.py
import os

def test_bounced_emails_file():
    path = '/home/user/bounced_emails.txt'
    assert os.path.isfile(path), f"File {path} does not exist. Did you extract the emails and save them?"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected = [
        "admin@nowhere.com",
        "charlie@bad-domain.net",
        "zack@bounced.org"
    ]

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert lines == expected, f"File {path} does not contain the expected sorted list of bounced emails. Found: {lines}"

def test_processed_logs_exists():
    path = '/home/user/app/processed_logs.txt'
    assert os.path.isfile(path), f"File {path} does not exist. The service may not have run successfully."

    with open(path, 'r') as f:
        content = f.read()

    assert "STATUS: 250 Delivered" in content and "STATUS: 550 Bounced" in content, \
        "The processed_logs.txt does not seem to contain the expected server output."

def test_run_service_modified():
    path = '/home/user/app/run_service.sh'
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "Europe/Berlin" in content, "TZ=Europe/Berlin does not appear to be exported in run_service.sh"
    assert "de_DE.UTF-8" in content, "LC_TIME=de_DE.UTF-8 does not appear to be exported in run_service.sh"

def test_daemon_unmodified():
    path = '/home/user/app/daemon.py'
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "if os.environ.get('TZ') != 'Europe/Berlin':" in content, "daemon.py seems to have been modified. You were instructed not to modify it."
    assert "8080" in content, "daemon.py seems to have been modified (the port should remain 8080)."