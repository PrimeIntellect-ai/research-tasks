# test_final_state.py

import os
import subprocess
import shutil
import pytest

def test_bad_commit_txt():
    path = "/home/user/bad_commit.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        commit_hash = f.read().strip()

    assert len(commit_hash) >= 7, "Commit hash in bad_commit.txt is missing or too short."

    # Verify the commit message of the hash
    res = subprocess.run(
        ["git", "-C", "/home/user/uptime-monitor", "log", "--format=%B", "-n", "1", commit_hash],
        capture_output=True, text=True
    )
    assert res.returncode == 0, f"Git log failed for hash '{commit_hash}'. Is it a valid commit?"

    expected_msg = "Refactor calculation to avoid external dependencies"
    assert expected_msg in res.stdout, f"The commit '{commit_hash}' is not the correct bad commit."

def test_uptime_calc_sh_fixed():
    calc_path = "/home/user/uptime-monitor/uptime_calc.sh"
    assert os.path.exists(calc_path), f"Script {calc_path} does not exist."
    assert os.access(calc_path, os.X_OK), f"Script {calc_path} is not executable."

    # Test case 1: 999 / 1000
    res1 = subprocess.run([calc_path, "999", "1000"], capture_output=True, text=True)
    assert res1.returncode == 0, "uptime_calc.sh failed to execute."
    output1 = res1.stdout.strip()
    assert output1 == "99.90", f"Expected output '99.90' for '999 1000', but got '{output1}'."

    # Test case 2: 5 / 10
    res2 = subprocess.run([calc_path, "5", "10"], capture_output=True, text=True)
    assert res2.returncode == 0, "uptime_calc.sh failed to execute."
    output2 = res2.stdout.strip()
    assert output2 == "50.00", f"Expected output '50.00' for '5 10', but got '{output2}'."

def test_fuzz_test_sh():
    fuzz_path = "/home/user/uptime-monitor/fuzz_test.sh"
    calc_path = "/home/user/uptime-monitor/uptime_calc.sh"
    backup_path = "/home/user/uptime-monitor/uptime_calc.sh.bak"

    assert os.path.exists(fuzz_path), f"File {fuzz_path} does not exist."
    assert os.access(fuzz_path, os.X_OK), f"File {fuzz_path} is not executable."

    # Backup the current uptime_calc.sh
    shutil.copy2(calc_path, backup_path)

    try:
        # Simulate the precision loss bug (always outputs 0.00)
        with open(calc_path, "w") as f:
            f.write("#!/bin/bash\necho '0.00'\n")

        res_bug = subprocess.run([fuzz_path], capture_output=True)
        assert res_bug.returncode == 1, "fuzz_test.sh should exit with code 1 when uptime_calc.sh outputs '0.00' (bug present)."

        # Simulate the fixed script (always outputs a non-zero valid percentage)
        with open(calc_path, "w") as f:
            f.write("#!/bin/bash\necho '99.90'\n")

        res_fix = subprocess.run([fuzz_path], capture_output=True)
        assert res_fix.returncode == 0, "fuzz_test.sh should exit with code 0 when uptime_calc.sh outputs correctly."

    finally:
        # Restore the original uptime_calc.sh
        shutil.move(backup_path, calc_path)