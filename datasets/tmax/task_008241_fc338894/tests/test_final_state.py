# test_final_state.py
import os

EXPECTED_RESULTS = """data_00.csv: STABLE 43
data_01.csv: STABLE 33
data_02.csv: STABLE 19
data_03.csv: SINGULAR 25
data_04.csv: STABLE 25
data_05.csv: STABLE 27
data_06.csv: STABLE 15
data_07.csv: SINGULAR 15
data_08.csv: STABLE 28
data_09.csv: STABLE 26
data_10.csv: STABLE 13
data_11.csv: STABLE 28
data_12.csv: STABLE 7
data_13.csv: STABLE 26
data_14.csv: SINGULAR 44
data_15.csv: STABLE 28
data_16.csv: STABLE 34
data_17.csv: STABLE 7
data_18.csv: SINGULAR 26
data_19.csv: STABLE 22"""

def test_analyze_go_exists_and_uses_goroutines():
    go_file = '/home/user/analyze.go'
    assert os.path.isfile(go_file), f"Expected Go source file at {go_file} is missing."

    with open(go_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple check for goroutines
    assert "go " in content, "The Go program must use goroutines (could not find 'go ' keyword in analyze.go)."

def test_results_txt_matches_expected():
    results_file = '/home/user/results.txt'
    assert os.path.isfile(results_file), f"Expected results file at {results_file} is missing."

    with open(results_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_lines = [line.strip() for line in EXPECTED_RESULTS.strip().split('\n') if line.strip()]
    actual_lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.txt, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i+1}:\nExpected: {expected}\nGot: {actual}"