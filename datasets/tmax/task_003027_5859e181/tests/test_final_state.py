# test_final_state.py
import os

def test_extracted_logs_directory():
    dir_path = "/home/user/extracted_logs"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist or is not a directory."

def test_extracted_files_content():
    expected_files = {
        "startup.log": "System initialized normally.",
        "authorized_keys": "Warning: Disk usage high.",
        "status.txt": "All services running."
    }

    for filename, expected_content in expected_files.items():
        filepath = os.path.join("/home/user/extracted_logs", filename)
        assert os.path.exists(filepath), f"File {filepath} was not extracted (path traversal might not be mitigated properly)."

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except UnicodeDecodeError:
            pytest.fail(f"File {filepath} is not valid UTF-8. Encoding conversion failed.")

        assert content == expected_content, f"Content of {filename} does not match expected. Got: {content}"

def test_audit_log_contents():
    audit_path = "/home/user/extraction_audit.log"
    assert os.path.exists(audit_path), f"Audit log {audit_path} does not exist."

    with open(audit_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "EXTRACTED: startup.log",
        "EXTRACTED: authorized_keys",
        "EXTRACTED: status.txt"
    }

    assert set(lines) == expected_lines, f"Audit log contents do not match expected. Expected exactly {expected_lines}, but got: {set(lines)}"

def test_script_logic():
    # Search for the script in /home/user/ to verify constraints
    found_flock = False
    found_iconv = False
    found_mv = False

    for root, dirs, files in os.walk("/home/user"):
        if "extracted_logs" in root:
            continue
        for file in files:
            if file in ["backup_archive.txt", "extraction_audit.log", ".bash_history", ".bashrc", ".profile", ".bash_logout"]:
                continue

            filepath = os.path.join(root, file)
            if not os.path.isfile(filepath):
                continue

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "flock" in content:
                        found_flock = True
                    if "iconv" in content:
                        found_iconv = True
                    if "mv " in content:
                        found_mv = True
            except Exception:
                pass

    assert found_flock, "Could not find 'flock' command in any script in /home/user/ (required for concurrent audit logging)."
    assert found_iconv, "Could not find 'iconv' command in any script in /home/user/ (required for encoding conversion)."
    assert found_mv, "Could not find 'mv' command in any script in /home/user/ (required for atomic writes)."