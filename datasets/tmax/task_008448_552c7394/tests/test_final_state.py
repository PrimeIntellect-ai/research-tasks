# test_final_state.py
import os
import json
import subprocess

def test_run_sh_exists_and_executable():
    run_sh_path = '/home/user/project/run.sh'
    assert os.path.isfile(run_sh_path), f"{run_sh_path} does not exist"
    assert os.access(run_sh_path, os.X_OK), f"{run_sh_path} is not executable"

def test_execute_run_sh():
    run_sh_path = '/home/user/project/run.sh'
    # Run the script and ensure it succeeds
    result = subprocess.run([run_sh_path], cwd='/home/user/project', capture_output=True, text=True)
    assert result.returncode == 0, f"run.sh failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def test_duplicates_json_correctness():
    json_path = '/home/user/project/duplicates.json'
    assert os.path.isfile(json_path), f"{json_path} does not exist. Did the client generate it?"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Failed to parse {json_path} as JSON: {e}"

    groups = data.get('groups', [])
    assert len(groups) == 1, f"Expected exactly 1 duplicate group, got {len(groups)}"

    group = groups[0]
    paths = sorted(group.get('file_paths', []))

    expected_paths = sorted([
        "/home/user/project/test_data/file1.txt",
        "/home/user/project/test_data/file2.txt",
        "/home/user/project/test_data/subdir/file3.txt"
    ])

    assert paths == expected_paths, f"Expected duplicate paths to be {expected_paths}, got {paths}"

    # Check that small files (<15 bytes) and unique files are not included
    not_expected = [
        "/home/user/project/test_data/file4.txt",
        "/home/user/project/test_data/file5.txt",
        "/home/user/project/test_data/subdir/file6.txt"
    ]
    for p in not_expected:
        assert p not in paths, f"File {p} should not be in the duplicate group"

def test_required_files_exist():
    expected_files = [
        '/home/user/project/proto/fileorg.proto',
        '/home/user/project/go_server/main.go',
        '/home/user/project/go_server/server_test.go',
        '/home/user/project/client/main.go'
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Required file {f} is missing"