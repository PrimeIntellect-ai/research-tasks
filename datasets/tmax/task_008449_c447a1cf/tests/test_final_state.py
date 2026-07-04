# test_final_state.py
import os
import json
import subprocess

def test_bad_commit_hash():
    bad_commit_path = "/home/user/bad_commit.txt"
    expected_path = "/tmp/expected_bad_commit.txt"

    assert os.path.exists(bad_commit_path), f"{bad_commit_path} does not exist. Did you save the bad commit hash?"
    assert os.path.exists(expected_path), "Truth file missing from setup."

    with open(bad_commit_path, "r") as f:
        student_hash = f.read().strip()

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    assert student_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {student_hash}"

def test_solution_output():
    solution_path = "/home/user/solution.txt"
    assert os.path.exists(solution_path), f"{solution_path} does not exist. Did you save the solution?"

    with open(solution_path, "r") as f:
        solution = f.read().strip()

    assert solution == "2.09455148", f"Expected solution 2.09455148, but got {solution}"

def test_params_recovered():
    params_path = "/home/user/opt-repo/params.json"
    assert os.path.exists(params_path), f"{params_path} does not exist. Did you recover the deleted file?"

    with open(params_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{params_path} is not valid JSON."

    assert data.get("initial_guess") == 3.0, "params.json initial_guess does not match the original content."
    assert data.get("tolerance") == 1e-6, "params.json tolerance does not match the original content."
    assert data.get("max_iter") == 100, "params.json max_iter does not match the original content."

def test_main_go_fixed():
    main_go_path = "/home/user/opt-repo/main.go"
    assert os.path.exists(main_go_path), f"{main_go_path} does not exist."

    repo_path = "/home/user/opt-repo"
    result = subprocess.run(
        ["go", "run", "main.go", "params.json"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"main.go failed to run: {result.stderr or result.stdout}. Did you fix the mathematical bug?"
    output = result.stdout.strip()
    assert output == "2.09455148", f"main.go output {output} instead of the expected 2.09455148. The mathematical bug may not be fully fixed."