# test_final_state.py
import os

def generate_golden_output():
    input_path = '/home/user/raw_data.txt'
    if not os.path.exists(input_path):
        return None

    with open(input_path, 'r') as f:
        data = [float(line.strip()) for line in f if line.strip()]

    if not data:
        return []

    N = len(data)
    min_val = min(data)
    max_val = max(data)

    tokens = []
    for x in data:
        if x == max_val:
            tokens.append(255)
        else:
            tokens.append(int((x - min_val) / (max_val - min_val) * 255))

    state = 42
    def my_rand():
        nonlocal state
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        return state

    bootstrapped = []
    for _ in range(N):
        idx = my_rand() % N
        bootstrapped.append(tokens[idx])

    return bootstrapped

def test_c_source_exists():
    path = '/home/user/prepare_data.c'
    assert os.path.exists(path), f"Source file {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_executable_exists():
    path = '/home/user/prepare_data'
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_output_file_exists():
    path = '/home/user/bootstrapped_tokens.txt'
    assert os.path.exists(path), f"Output file {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_output_contents():
    output_path = '/home/user/bootstrapped_tokens.txt'
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    golden_tokens = generate_golden_output()
    assert golden_tokens is not None, "Could not generate golden output because input file is missing."

    with open(output_path, 'r') as f:
        user_lines = [line.strip() for line in f if line.strip()]

    assert len(user_lines) == len(golden_tokens), f"Expected {len(golden_tokens)} lines in output, found {len(user_lines)}."

    for i, (user_val, expected_val) in enumerate(zip(user_lines, golden_tokens)):
        try:
            user_int = int(user_val)
        except ValueError:
            assert False, f"Line {i+1} in output is not a valid integer: {user_val}"

        assert user_int == expected_val, f"Mismatch at line {i+1}: expected {expected_val}, got {user_int}"