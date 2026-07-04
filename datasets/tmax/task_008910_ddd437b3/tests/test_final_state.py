# test_final_state.py

import os
import subprocess

def test_regression_commit_file():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/regression_commit.txt"

    assert os.path.exists(expected_file), f"Expected commit file {expected_file} is missing."
    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    assert os.path.exists(actual_file), f"The file {actual_file} does not exist."
    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected commit hash {expected_hash}, but got {actual_hash}."

def test_git_branch_is_main():
    repo_path = "/home/user/data-parser"
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to get current git branch."
    assert result.stdout.strip() == "main", f"Repository is on branch '{result.stdout.strip()}', expected 'main'."

def test_parser_go_fixed():
    parser_path = "/home/user/data-parser/parser.go"
    assert os.path.exists(parser_path), f"File {parser_path} is missing."
    with open(parser_path, "r") as f:
        content = f.read()

    assert "base64.StdEncoding.DecodeString" in content, "parser.go does not contain the fix (base64.StdEncoding.DecodeString)."
    assert "base64.URLEncoding.DecodeString" not in content, "parser.go still contains the buggy base64.URLEncoding."

def test_go_run_success():
    repo_path = "/home/user/data-parser"
    payload_path = "/home/user/payload.txt"

    env = os.environ.copy()
    env["CGO_ENABLED"] = "1"

    # Use 'go run .' to include all files in the main package
    result = subprocess.run(
        ["go", "run", ".", "-f", payload_path],
        cwd=repo_path,
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"go run failed. Return code: {result.returncode}\nStderr: {result.stderr}\nStdout: {result.stdout}"

    expected_output = "Decoded: Hello World!/test+data="
    assert expected_output in result.stdout, f"Output did not contain the expected decoded string.\nGot: {result.stdout}"