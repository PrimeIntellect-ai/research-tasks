# test_final_state.py

import os

def test_go_program_exists():
    assert os.path.isfile("/home/user/audit_archives.go"), "The Go program /home/user/audit_archives.go was not found."

def test_archives_not_deleted():
    expected_files = [
        "/home/user/uploaded_archives/project_a/clean1.zip",
        "/home/user/uploaded_archives/project_a/malicious1.zip",
        "/home/user/uploaded_archives/project_b/clean2.tar",
        "/home/user/uploaded_archives/project_b/nested/malicious2.tar",
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Archive file missing, perhaps the cleanup script was executed: {f}"

def test_malicious_archives_log():
    log_file = "/home/user/malicious_archives.log"
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/uploaded_archives/project_a/malicious1.zip",
        "/home/user/uploaded_archives/project_b/nested/malicious2.tar"
    ]

    # Check if lines match exactly, including alphabetical sorting
    assert lines == expected_lines, f"Contents of {log_file} do not match the expected sorted list of malicious archives. Got: {lines}"

def test_cleanup_script():
    script_file = "/home/user/cleanup.sh"
    assert os.path.isfile(script_file), f"Cleanup script missing: {script_file}"

    with open(script_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 3, f"Cleanup script {script_file} does not have enough lines."
    assert lines[0] == "#!/bin/bash", f"Cleanup script does not start with #!/bin/bash shebang. Got: {lines[0]}"

    expected_commands = [
        "rm -f '/home/user/uploaded_archives/project_a/malicious1.zip'",
        "rm -f '/home/user/uploaded_archives/project_b/nested/malicious2.tar'"
    ]

    assert lines[1:] == expected_commands, f"Cleanup script commands do not match expected output. Got: {lines[1:]}"