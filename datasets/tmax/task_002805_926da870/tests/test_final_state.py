# test_final_state.py
import os

def test_query_tool_exists_and_parameterized():
    script_path = '/home/user/query_tool.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert '?' in content, "The script does not appear to use parameterized queries (missing '?' placeholders)."

def test_q1_output():
    output_path = '/home/user/q1_output.txt'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ['T003', 'T001']
    assert lines == expected, f"Q1 output incorrect. Expected {expected}, got {lines}."

def test_q2_output():
    output_path = '/home/user/q2_output.txt'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ['T008', 'T005', 'T002']
    assert lines == expected, f"Q2 output incorrect. Expected {expected}, got {lines}."