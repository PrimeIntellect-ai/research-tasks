# test_final_state.py

import os
import subprocess
import pytest

REPO_DIR = "/home/user/prng_repo"
HASH_FILE = "/home/user/bad_commit_hash.txt"
PATCH_FILE = "/home/user/fix.patch"

def run_git_command(args, cwd=REPO_DIR):
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def test_bad_commit_hash_correct():
    assert os.path.isfile(HASH_FILE), f"File {HASH_FILE} does not exist."

    with open(HASH_FILE, "r") as f:
        actual_hash = f.read().strip()

    expected_hash = run_git_command(["log", "--grep=Optimize bitmask and refactor step 137", "--format=%H"])

    assert actual_hash == expected_hash, f"Incorrect bad commit hash in {HASH_FILE}. Expected {expected_hash}, got {actual_hash}."

def test_patch_exists_and_fixes_bug(tmp_path):
    assert os.path.isfile(PATCH_FILE), f"Patch file {PATCH_FILE} does not exist."

    # Clone the repo to a temporary directory to avoid messing with the student's working tree
    temp_repo = tmp_path / "prng_repo"
    subprocess.run(["git", "clone", REPO_DIR, str(temp_repo)], check=True, capture_output=True)

    # Ensure we are on the latest commit before the student's fix if they committed it, 
    # but the instructions say "latest main branch". The student might have committed the fix.
    # We will just apply the patch to the current HEAD of their repo (which we cloned).
    # If they already committed the fix, the patch might not apply, or it might be empty.
    # The prompt says "Ensure that your fix ... and that the patch applies cleanly to the latest main branch."
    # Let's test if we can apply the patch. If the patch is already applied, maybe they diffed against HEAD~1.
    # The safest way is to just run `git apply` or `patch` and check the output.

    # Actually, let's just restore the bad state in the temp repo to be sure, or just reset hard.
    subprocess.run(["git", "reset", "--hard", "HEAD"], cwd=str(temp_repo), check=True, capture_output=True)

    # Apply the patch
    apply_proc = subprocess.run(["git", "apply", PATCH_FILE], cwd=str(temp_repo), capture_output=True, text=True)
    assert apply_proc.returncode == 0, f"Patch failed to apply cleanly:\n{apply_proc.stderr}"

    # Test the output of the PRNG
    python_code = "import prng; print(prng.generate(42, 3))"
    py_proc = subprocess.run(["python3", "-c", python_code], cwd=str(temp_repo), capture_output=True, text=True)

    expected_output = "[1804289383, 846930886, 1681692777]"
    actual_output = py_proc.stdout.strip()

    assert actual_output == expected_output, f"Patch did not restore the correct mathematical behavior. Expected {expected_output}, got {actual_output}."