# test_final_state.py
import os

def test_result_file_exists_and_correct():
    result_path = '/home/user/result.txt'
    assert os.path.isfile(result_path), f"The output file {result_path} does not exist. Did you run the script?"

    with open(result_path, 'r') as f:
        result = f.read().strip()

    assert result == "5.0250", f"Expected result '5.0250', but got '{result}'. Check your vectorization logic."

def test_script_is_vectorized():
    script_path = '/home/user/analyze_signal.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

    with open(script_path, 'r') as f:
        code = f.read()

    assert "for d in data:" not in code, "The nested loop 'for d in data:' was found. The function must be fully vectorized."
    assert "for i, x in enumerate(x_grid):" not in code, "The loop over x_grid was found. The function must be fully vectorized."