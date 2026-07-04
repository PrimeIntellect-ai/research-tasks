# test_final_state.py

import os

def test_extracted_files_exist():
    """Test that the files have been extracted correctly."""
    extracted_dir = "/home/user/extracted"
    assert os.path.exists(extracted_dir), f"Directory {extracted_dir} does not exist."

    expected_files = ["sensor_read", "web_server", "data_logger", "notes.txt", "model.gcode"]
    for f in expected_files:
        path = os.path.join(extracted_dir, f)
        assert os.path.exists(path), f"Extracted file {path} is missing."
        assert os.path.isfile(path), f"{path} is not a file."

def test_symlinks_created_correctly():
    """Test that the symlinks are correctly created in the organized_elfs directory."""
    arm_dir = "/home/user/organized_elfs/ARM"
    x86_dir = "/home/user/organized_elfs/x86_64"

    assert os.path.exists(arm_dir), f"Directory {arm_dir} does not exist."
    assert os.path.exists(x86_dir), f"Directory {x86_dir} does not exist."

    expected_symlinks = {
        os.path.join(arm_dir, "sensor_read"): "/home/user/extracted/sensor_read",
        os.path.join(arm_dir, "data_logger"): "/home/user/extracted/data_logger",
        os.path.join(x86_dir, "web_server"): "/home/user/extracted/web_server"
    }

    for symlink, target in expected_symlinks.items():
        assert os.path.islink(symlink), f"Expected symlink at {symlink} is missing or not a symlink."
        actual_target = os.readlink(symlink)
        assert actual_target == target, f"Symlink {symlink} points to {actual_target}, expected {target}."

def test_script_exists():
    """Test that the organize_elfs.py script exists."""
    script_path = "/home/user/organize_elfs.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_log_file_contents():
    """Test that the log file contains the correct paths, sorted alphabetically."""
    log_path = "/home/user/elf_inventory.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    expected_lines = [
        "/home/user/organized_elfs/ARM/data_logger\n",
        "/home/user/organized_elfs/ARM/sensor_read\n",
        "/home/user/organized_elfs/x86_64/web_server\n"
    ]

    with open(log_path, "r") as f:
        actual_lines = f.readlines()

    # Strip trailing newlines for comparison in case of formatting differences, 
    # but ensure the order and content is correct.
    actual_lines_stripped = [line.strip() for line in actual_lines if line.strip()]
    expected_lines_stripped = [line.strip() for line in expected_lines]

    assert actual_lines_stripped == expected_lines_stripped, (
        f"Log file contents are incorrect.\nExpected: {expected_lines_stripped}\nActual: {actual_lines_stripped}"
    )