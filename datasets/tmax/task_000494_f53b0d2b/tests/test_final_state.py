# test_final_state.py
import os

def test_nfs_monitor_cpp_exists():
    assert os.path.isfile("/home/user/nfs_monitor.cpp"), "/home/user/nfs_monitor.cpp does not exist."

def test_check_mounts_sh_exists_and_content():
    script_path = "/home/user/check_mounts.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()
    assert "set -e" in content, f"{script_path} does not contain 'set -e'."
    assert "g++" in content, f"{script_path} does not contain 'g++'."

def test_outbox_directory_exists():
    assert os.path.isdir("/home/user/outbox"), "/home/user/outbox/ directory does not exist."

def test_alert_files():
    outbox_dir = "/home/user/outbox"

    expected_files = [
        "alert_broken-server.invalid.txt",
        "alert_unreachable-node.localdomain.invalid.txt"
    ]

    # Check that exactly these two .txt files exist
    txt_files = [f for f in os.listdir(outbox_dir) if f.endswith(".txt")]
    assert len(txt_files) == 2, f"Expected exactly 2 .txt files in outbox, found {len(txt_files)}: {txt_files}"

    for expected_file in expected_files:
        assert expected_file in txt_files, f"Expected file {expected_file} not found in outbox."

        hostname = expected_file.replace("alert_", "").replace(".txt", "")
        expected_content = (
            "To: netops@domain.local\n"
            "From: monitor@domain.local\n"
            f"Subject: Unreachable NFS Host: {hostname}\n"
            "\n"
            f"Error: {hostname} failed DNS resolution.\n"
        )

        file_path = os.path.join(outbox_dir, expected_file)
        with open(file_path, "r") as f:
            content = f.read()

        assert content.strip() == expected_content.strip(), f"Content of {expected_file} does not match expected output."