# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_bad_commit_hash_correct():
    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} does not exist."

    with open(bad_commit_file, "r") as f:
        student_hash = f.read().strip()

    repo_dir = "/home/user/sorter_repo"
    try:
        result = subprocess.run(
            ["git", "-C", repo_dir, "log", "--format=%H", "--grep=Commit 137"],
            capture_output=True, text=True, check=True
        )
        expected_hash = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query git repository for the bad commit: {e.stderr}")

    assert expected_hash, "Could not find the expected bad commit in the repository."
    assert student_hash == expected_hash, f"Incorrect commit hash in {bad_commit_file}. Expected {expected_hash}, got {student_hash}"

def test_fixed_sort_c_compiles_and_sorts():
    fixed_sort = "/home/user/fixed_sort.c"
    assert os.path.isfile(fixed_sort), f"File {fixed_sort} does not exist."

    repo_dir = "/home/user/sorter_repo"
    main_c = os.path.join(repo_dir, "main.c")
    assert os.path.isfile(main_c), f"Original main.c is missing from {repo_dir}."

    with tempfile.TemporaryDirectory() as tmpdir:
        out_bin = os.path.join(tmpdir, "sorter")

        # Compile the student's fixed_sort.c with the original main.c
        compile_res = subprocess.run(
            ["gcc", "-O0", "-g", main_c, fixed_sort, "-o", out_bin],
            capture_output=True, text=True
        )
        assert compile_res.returncode == 0, f"Compilation of fixed_sort.c failed:\n{compile_res.stderr}"

        # Test with a sequence that would trigger the issue or verify correctness
        test_inputs = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
        try:
            run_res = subprocess.run(
                [out_bin] + test_inputs,
                capture_output=True, text=True, timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail("The compiled program timed out (likely infinite recursion/hang is still present).")

        assert run_res.returncode == 0, f"Program crashed or returned non-zero exit status:\n{run_res.stderr}"

        output = run_res.stdout.strip()
        expected_output = " ".join(sorted(test_inputs, key=int))
        assert output == expected_output, f"Sorting output is incorrect. Expected '{expected_output}', but got '{output}'."