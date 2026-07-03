# test_final_state.py
import os
import subprocess
import tempfile

def test_robust_filter_accuracy():
    agent_script = "/home/user/robust_filter.py"
    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(agent_script), f"{agent_script} is not a file"

    # Create a test log file with edge cases
    test_log_content = """\
123 abc racecar def
456 def hello world
789 ghi level jkl
101 jkl noon mno
112 mno a pqr
131 pqr radar stu
long_line_start """ + "a" * 150 + """ kayak end
short
another_long_line """ + "b" * 150 + """ notpalindrome end
"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(test_log_content)
        test_file = f.name

    try:
        column = 3

        # Expected logic
        expected_lines = []
        with open(test_file, 'r') as f:
            for line in f:
                words = line.strip('\n').split()
                if 0 <= column - 1 < len(words):
                    word = words[column - 1]
                    if len(word) >= 2 and word == word[::-1]:
                        expected_lines.append(line.strip('\n'))

        # Agent output
        try:
            res = subprocess.run(['python3', agent_script, str(column), test_file], capture_output=True, text=True, timeout=10)
            agent_lines = [l for l in res.stdout.split('\n') if l]
        except subprocess.TimeoutExpired:
            assert False, "Agent script timed out."
        except Exception as e:
            assert False, f"Agent script failed to run: {e}"

        expected_set = set(expected_lines)
        agent_set = set(agent_lines)

        true_positives = len(expected_set & agent_set)
        false_positives = len(agent_set - expected_set)
        false_negatives = len(expected_set - agent_set)

        if true_positives == 0 and (false_positives > 0 or false_negatives > 0):
            f1 = 0.0
        elif true_positives == 0:
            f1 = 1.0
        else:
            precision = true_positives / (true_positives + false_positives)
            recall = true_positives / (true_positives + false_negatives)
            f1 = 2 * (precision * recall) / (precision + recall)

        assert f1 >= 1.0, f"F1 score {f1} is below threshold 1.0. Expected lines: {expected_set}, Agent lines: {agent_set}"
    finally:
        os.remove(test_file)