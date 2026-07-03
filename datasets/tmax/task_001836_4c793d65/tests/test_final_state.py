# test_final_state.py
import os
import pytest

def test_combined_v2_json_content():
    combined_path = '/home/user/combined_v2.json'
    assert os.path.isfile(combined_path), f"File {combined_path} does not exist."

    with open(combined_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_content = (
        '{"sensor": "B", "val": 20}\n'
        '{"sensor": "B", "val": 21}\n'
        '{"sensor": "C", "val": 30}\n'
        '{"sensor": "C", "val": 31}\n'
        '{"sensor": "C", "val": 32}\n'
        '{"sensor": "E", "val": 50}'
    )

    assert content == expected_content, f"Content of {combined_path} is incorrect. Got:\n{content}"

def test_summary_txt_content():
    summary_path = '/home/user/summary.txt'
    assert os.path.isfile(summary_path), f"File {summary_path} does not exist."

    with open(summary_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {summary_path}, got {len(lines)}."
    assert lines[0] == '3', f"Expected first line of {summary_path} to be '3', got '{lines[0]}'."
    assert lines[1] == '6', f"Expected second line of {summary_path} to be '6', got '{lines[1]}'."

def test_script_uses_flock():
    script_path = '/home/user/process_archives.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'flock' in content, f"The script {script_path} must use 'flock' to acquire a lock."