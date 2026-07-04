# test_final_state.py
import os

def get_nth_prime(n):
    if n <= 0: return 0
    count = 0
    current = 1
    while count < n:
        current += 1
        is_prime = True
        for i in range(2, int(current**0.5) + 1):
            if current % i == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return current

def get_distinct_prime_factors_count(n):
    count = 0
    d = 2
    num = n
    while num > 1:
        if num % d == 0:
            count += 1
            while num % d == 0:
                num //= d
        d += 1
        if d * d > num and num > 1:
            count += 1
            break
    return count

def evaluate_program(filepath):
    acc = 0
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split()
            if len(parts) != 2: continue
            cmd = parts[0]
            val = int(parts[1])
            if cmd == 'ADD':
                acc += val
            elif cmd == 'MUL':
                acc *= val
            elif cmd == 'PRIME':
                acc += get_nth_prime(val)
            elif cmd == 'FACTORS':
                acc += get_distinct_prime_factors_count(val)
    return acc

def test_c_binary_compiled():
    c_bin = "/home/user/project/libmath/prime"
    assert os.path.isfile(c_bin), "C binary 'prime' was not successfully compiled in /home/user/project/libmath/."
    assert os.access(c_bin, os.X_OK), "The compiled C file 'prime' is not executable."

def test_rust_binary_compiled():
    rs_bin = "/home/user/project/rs_calc/target/release/rs_calc"
    assert os.path.isfile(rs_bin), "Rust binary 'rs_calc' was not successfully compiled in release mode."
    assert os.access(rs_bin, os.X_OK), "The compiled Rust file 'rs_calc' is not executable."

def test_result_file_exists_and_correct():
    result_file = "/home/user/project/result.txt"
    program_file = "/home/user/project/program.math"

    assert os.path.isfile(program_file), "The program.math file is missing."
    assert os.path.isfile(result_file), "The result.txt file was not created by the Go program."

    expected_result = evaluate_program(program_file)

    with open(result_file, 'r') as f:
        content = f.read().strip()

    assert content.isdigit() or (content.startswith('-') and content[1:].isdigit()), f"result.txt does not contain a valid integer. Found: {content}"
    actual_result = int(content)

    assert actual_result == expected_result, f"Expected final accumulator value to be {expected_result}, but got {actual_result}."