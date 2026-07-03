# test_final_state.py
import os
import subprocess
import re
import pytest

def test_min_crash_file():
    min_crash_path = '/home/user/min_crash.txt'
    assert os.path.isfile(min_crash_path), f"{min_crash_path} does not exist"

    with open(min_crash_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, "min_crash.txt should contain exactly 3 lines"

    # Match TX <id> ACTION
    pattern = re.compile(r'^TX\s+(\d+)\s+([A-Z]+)$')

    match1 = pattern.match(lines[0])
    assert match1, "Line 1 does not match expected format 'TX <id> ACTION'"
    id1, action1 = match1.groups()
    assert action1 == "BEGIN", "First command must be BEGIN"

    match2 = pattern.match(lines[1])
    assert match2, "Line 2 does not match expected format 'TX <id> ACTION'"
    id2, action2 = match2.groups()
    assert action2 in ("ABORT", "COMMIT"), "Second command must be ABORT or COMMIT"

    match3 = pattern.match(lines[2])
    assert match3, "Line 3 does not match expected format 'TX <id> ACTION'"
    id3, action3 = match3.groups()
    assert action3 in ("ABORT", "COMMIT"), "Third command must be ABORT or COMMIT"

    assert id1 == id2 == id3, "Transaction IDs must be identical across all three lines"

def test_recover_fixed_and_compiled():
    # Recompile to ensure db_recover is up to date
    make_clean = subprocess.run(['make', 'clean'], cwd='/home/user', capture_output=True)
    make_build = subprocess.run(['make'], cwd='/home/user', capture_output=True)
    assert make_build.returncode == 0, "Failed to compile db_recover"

    db_recover_path = '/home/user/db_recover'
    assert os.path.isfile(db_recover_path), "db_recover executable not found after make"

    # Test with min_crash.txt
    min_crash_path = '/home/user/min_crash.txt'
    with open(min_crash_path, 'r') as f:
        crash_data = f.read()

    run_min_crash = subprocess.run(
        [db_recover_path],
        input=crash_data.encode('utf-8'),
        cwd='/home/user',
        capture_output=True
    )
    assert run_min_crash.returncode == 0, "db_recover crashed or returned non-zero when processing min_crash.txt"

    # Test with a guaranteed double-free sequence to ensure the C code bug was actually fixed
    test_sequence = "TX 99 BEGIN\nTX 99 COMMIT\nTX 99 ABORT\n"
    run_test_seq = subprocess.run(
        [db_recover_path],
        input=test_sequence.encode('utf-8'),
        cwd='/home/user',
        capture_output=True
    )
    assert run_test_seq.returncode == 0, "db_recover crashed on a double-free sequence, bug is not fully fixed"