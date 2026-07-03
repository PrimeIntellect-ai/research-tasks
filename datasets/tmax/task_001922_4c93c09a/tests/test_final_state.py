# test_final_state.py
import os

def test_crash_input_file():
    path = "/home/user/crash_input.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you write the crash input to it?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "-42069", f"Expected crash_input.txt to contain '-42069', but found '{content}'."

def test_final_result_file():
    path = "/home/user/final_result.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you write the final result to it?"

    with open(path, "r") as f:
        content = f.read().strip()

    # Compute the expected sum
    expected_sum = 0
    for n in range(-100000, 100001):
        if n == -42069:
            val = 0
        else:
            val = (n ** 2) % 1000
        expected_sum += val

    assert content == str(expected_sum), f"Expected final_result.txt to contain '{expected_sum}', but found '{content}'."

def test_calc_series_script_fixes():
    path = "/home/user/calc_series.py"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "ThreadPoolExecutor" in content, "The script must still use ThreadPoolExecutor for concurrency."
    assert "calculate_all" in content, "The script must still define calculate_all."