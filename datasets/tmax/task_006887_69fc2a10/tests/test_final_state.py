# test_final_state.py
import os
import json

def test_script_exists_and_executable():
    script_path = '/home/user/pipeline/run_etl.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_results_jsonl_exists_and_correct():
    results_path = '/home/user/pipeline/results.jsonl'
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    expected_objects = [
        {"user":"alice","repo":"repoA","file":"main.py","library":"requests"},
        {"user":"alice","repo":"repoA","file":"main.py","library":"sys"},
        {"user":"alice","repo":"repoA","file":"utils.py","library":"os"},
        {"user":"alice","repo":"repoC","file":"index.ts","library":"lodash"},
        {"user":"bob","repo":"repoB","file":"app.js","library":"express"},
        {"user":"charlie","repo":"repoC","file":"index.ts","library":"lodash"}
    ]

    actual_objects = []
    with open(results_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                actual_objects.append(obj)
            except json.JSONDecodeError:
                assert False, f"Line {line_num} in {results_path} is not valid JSON."

    assert len(actual_objects) == len(expected_objects), f"Expected {len(expected_objects)} lines in {results_path}, got {len(actual_objects)}."

    # Compare independent of order
    def sort_key(obj):
        return (obj.get("user", ""), obj.get("repo", ""), obj.get("file", ""), obj.get("library", ""))

    actual_sorted = sorted(actual_objects, key=sort_key)
    expected_sorted = sorted(expected_objects, key=sort_key)

    assert actual_sorted == expected_sorted, "The extracted graph patterns in results.jsonl do not match the expected output."