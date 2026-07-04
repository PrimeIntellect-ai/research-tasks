# test_final_state.py
import os
import pathlib

def test_safe_files_extracted():
    config_root = pathlib.Path("/home/user/config_root")

    safe_config = config_root / "safe_config.ini"
    assert safe_config.is_file(), f"Expected safe file {safe_config} was not extracted."
    with open(safe_config, "rb") as f:
        assert f.read() == b"safe content", f"Content of {safe_config} is incorrect."

    safe_dir = config_root / "safe_dir"
    assert safe_dir.is_dir(), f"Expected safe directory {safe_dir} was not extracted."

    safe_symlink = config_root / "safe_symlink"
    assert safe_symlink.is_symlink(), f"Expected safe symlink {safe_symlink} was not extracted as a symlink."
    assert os.readlink(safe_symlink) == "safe_config.ini", f"Symlink {safe_symlink} has incorrect target."

def test_unsafe_files_not_extracted():
    # Check that zip slip files didn't escape
    evil1 = pathlib.Path("/home/user/evil1.txt")
    assert not evil1.exists(), f"Zip slip vulnerability! {evil1} was extracted outside the target directory."

    evil2 = pathlib.Path("/home/evil2.txt")
    assert not evil2.exists(), f"Zip slip vulnerability! {evil2} was extracted outside the target directory."

    # Check that unsafe symlink/hardlink weren't extracted
    config_root = pathlib.Path("/home/user/config_root")
    unsafe_sym = config_root / "unsafe_symlink"
    assert not unsafe_sym.exists(), f"Unsafe symlink {unsafe_sym} should not have been extracted."

    unsafe_hard = config_root / "unsafe_hardlink"
    assert not unsafe_hard.exists(), f"Unsafe hardlink {unsafe_hard} should not have been extracted."

def test_security_log_contents():
    log_file = pathlib.Path("/home/user/security.log")
    assert log_file.is_file(), f"Log file {log_file} was not created."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_skipped = {
        "/home/user/evil1.txt",
        "safe_dir/../../evil2.txt",
        "unsafe_symlink",
        "unsafe_hardlink"
    }

    actual_skipped = set(lines)

    missing = expected_skipped - actual_skipped
    extra = actual_skipped - expected_skipped

    assert not missing, f"Log file is missing entries for skipped files: {missing}"
    assert not extra, f"Log file contains unexpected entries: {extra}"
    assert len(lines) == len(expected_skipped), "Log file contains duplicate entries."