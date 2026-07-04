# test_final_state.py

import os
import stat
import pytest

def get_dir_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def test_script_exists_and_executable():
    script_path = "/home/user/enforce_quota.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_bob_untouched():
    bob_dir = "/home/user/ci_builds/bob"
    assert os.path.isdir(bob_dir), "Bob's directory is missing."

    build_log = os.path.join(bob_dir, "build.log")
    app_jar = os.path.join(bob_dir, "app.jar")

    assert os.path.isfile(build_log), "Bob's build.log was incorrectly deleted."
    assert os.path.isfile(app_jar), "Bob's app.jar was incorrectly deleted."

def test_alice_quota_and_files():
    alice_dir = "/home/user/ci_builds/alice"
    assert os.path.isdir(alice_dir), "Alice's directory is missing."

    size = get_dir_size(alice_dir)
    assert size <= 40000000, f"Alice's directory size {size} exceeds quota 40000000."

    old_build = os.path.join(alice_dir, "old_build.o")
    cache = os.path.join(alice_dir, "cache.pyc")
    main_bin = os.path.join(alice_dir, "main.bin")

    assert not os.path.exists(old_build), "Alice's old_build.o should have been deleted."
    assert not os.path.exists(cache), "Alice's cache.pyc should have been deleted."
    assert os.path.isfile(main_bin), "Alice's main.bin should have been kept."

def test_charlie_quota_and_files():
    charlie_dir = "/home/user/ci_builds/charlie"
    assert os.path.isdir(charlie_dir), "Charlie's directory is missing."

    size = get_dir_size(charlie_dir)
    assert size <= 40000000, f"Charlie's directory size {size} exceeds quota 40000000."

    lib1 = os.path.join(charlie_dir, "lib1.so")
    lib2 = os.path.join(charlie_dir, "lib2.so")

    assert not os.path.exists(lib1), "Charlie's lib1.so should have been deleted."
    assert os.path.isfile(lib2), "Charlie's lib2.so should have been kept."

def test_log_file_contents():
    log_file = "/home/user/quota_cleanup.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    expected_lines = [
        "[CLEANUP] Deleted /home/user/ci_builds/alice/old_build.o recovered 15728640 bytes from alice",
        "[CLEANUP] Deleted /home/user/ci_builds/alice/cache.pyc recovered 15728640 bytes from alice",
        "[CLEANUP] Deleted /home/user/ci_builds/charlie/lib1.so recovered 26214400 bytes from charlie"
    ]

    for line in expected_lines:
        assert line in content, f"Expected log line not found: '{line}'"