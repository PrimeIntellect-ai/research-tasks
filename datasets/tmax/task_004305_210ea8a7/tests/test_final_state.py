# test_final_state.py
import os
import hashlib
import pytest

def test_malicious_paths_log():
    log_path = '/home/user/malicious_paths.log'
    assert os.path.exists(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_paths = {
        '../../etc/passwd_fake',
        '/absolute/path/escape.sh'
    }

    assert set(lines) == expected_paths, f"Expected malicious paths {expected_paths}, but got {set(lines)}"

def test_project_workspace_state():
    workspace = '/home/user/project_workspace'

    readme_path = os.path.join(workspace, 'README.md')
    app_go_path = os.path.join(workspace, 'src', 'app.go')
    main_go_path = os.path.join(workspace, 'src', 'main.go')

    # Check README.md
    assert os.path.exists(readme_path), f"{readme_path} does not exist."
    with open(readme_path, 'r') as f:
        content = f.read()
    assert content == "# Project\nUpdated README", f"Incorrect content in {readme_path}"

    # Check src/app.go
    assert os.path.exists(app_go_path), f"{app_go_path} does not exist."
    with open(app_go_path, 'r') as f:
        content = f.read()
    assert content == "package main\n// App", f"Incorrect content in {app_go_path}"

    # Check src/main.go
    assert not os.path.exists(main_go_path), f"{main_go_path} should have been deleted."

def test_manifest_txt():
    manifest_path = '/home/user/manifest.txt'
    assert os.path.exists(manifest_path), f"File {manifest_path} does not exist."

    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_readme_hash = hashlib.sha256(b"# Project\nUpdated README").hexdigest()
    expected_app_hash = hashlib.sha256(b"package main\n// App").hexdigest()

    expected_lines = [
        f"README.md  {expected_readme_hash}",
        f"src/app.go  {expected_app_hash}"
    ]

    # Check exact lines and order
    assert lines == expected_lines, f"Expected manifest lines {expected_lines}, but got {lines}"