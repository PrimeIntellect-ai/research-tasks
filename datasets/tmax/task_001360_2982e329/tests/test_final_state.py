# test_final_state.py

import os
import pytest

def test_verify_c_exists_and_contains_required_syscalls():
    verify_c_path = "/home/user/verify.c"
    assert os.path.isfile(verify_c_path), f"Missing C source file: {verify_c_path}"

    with open(verify_c_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "mmap" in content, "The program must use mmap to read hashes.bin"

    has_flock = "flock" in content
    has_fcntl = "F_SETLK" in content or "F_SETLKW" in content
    assert has_flock or has_fcntl, "The program must use file locking (flock or fcntl) before writing to the log"

def test_verified_log_contents():
    log_path = "/home/user/verified.log"
    assert os.path.isfile(log_path), f"Missing log file: {log_path}"

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert set(lines) == {"main.c", "utils.c"}, f"verified.log should contain exactly main.c and utils.c, got: {lines}"

def test_src_files_modified_correctly():
    src_dir = "/home/user/src"

    main_c = os.path.join(src_dir, "main.c")
    utils_c = os.path.join(src_dir, "utils.c")
    bad_c = os.path.join(src_dir, "bad.c")

    assert os.path.isfile(main_c), f"Missing extracted file: {main_c}"
    assert os.path.isfile(utils_c), f"Missing extracted file: {utils_c}"
    assert os.path.isfile(bad_c), f"Missing extracted file: {bad_c}"

    with open(main_c, "r", encoding="utf-8") as f:
        main_content = f.read()
    assert "MODERN_API_CALL" in main_content, "main.c should have MODERN_API_CALL"
    assert "DEPRECATED_API_CALL" not in main_content, "main.c should not have DEPRECATED_API_CALL"

    with open(utils_c, "r", encoding="utf-8") as f:
        utils_content = f.read()
    assert "MODERN_API_CALL" in utils_content, "utils.c should have MODERN_API_CALL"
    assert "DEPRECATED_API_CALL" not in utils_content, "utils.c should not have DEPRECATED_API_CALL"

    with open(bad_c, "r", encoding="utf-8") as f:
        bad_content = f.read()
    assert "DEPRECATED_API_CALL" in bad_content, "bad.c should still have DEPRECATED_API_CALL (it was corrupted)"
    assert "MODERN_API_CALL" not in bad_content, "bad.c should not have MODERN_API_CALL"