# test_final_state.py

import os
import time
import subprocess
import pytest

def generate_test_data(num_equations=100000):
    import random
    equations = []
    reference = []

    ops = ['+', '-', '*']
    for _ in range(num_equations):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = random.randint(1, 100)
        op1 = random.choice(ops)
        op2 = random.choice(ops)

        expr = f"( {a} {op1} {b} ) {op2} {c}"

        # calculate value
        try:
            val = eval(expr)
        except ZeroDivisionError:
            val = 0

        val_mod = val % 733

        # calculate checksum
        expr_no_space = expr.replace(" ", "")
        checksum = sum(ord(char) for char in expr_no_space)

        # occasionally make invalid checksum to test filtering
        if random.random() < 0.05:
            checksum += 1
        else:
            reference.append(f"{expr},{val_mod}")

        equations.append(f"{expr} | {checksum}")

    return equations, reference

def test_aud_eval_accuracy_and_speed():
    bin_path = "/home/user/aud-eval/bin/aud-eval"
    assert os.path.isfile(bin_path), f"Compiled binary not found at {bin_path}"

    equations, reference = generate_test_data(200000)

    test_file = "/home/user/aud-eval/test_equations.txt"
    with open(test_file, "w") as f:
        f.write("\n".join(equations) + "\n")

    # Try running with argument first, if it fails or ignores, we might need to overwrite equations.txt
    # The prompt says "process the 500,000 lines in equations.txt", so they might have hardcoded it.
    # Let's overwrite equations.txt to be safe.
    target_file = "/home/user/aud-eval/equations.txt"
    with open(target_file, "w") as f:
        f.write("\n".join(equations) + "\n")

    results_file = "/home/user/aud-eval/results.csv"
    if os.path.exists(results_file):
        os.remove(results_file)

    start_time = time.time()
    try:
        subprocess.run([bin_path, target_file], check=True, cwd="/home/user/aud-eval")
    except subprocess.CalledProcessError:
        # Fallback without argument
        subprocess.run([bin_path], check=True, cwd="/home/user/aud-eval")

    duration = time.time() - start_time

    assert os.path.isfile(results_file), f"Results file not found at {results_file}"

    with open(results_file, "r") as f:
        agent_lines = f.read().splitlines()

    correct = sum(1 for a, r in zip(agent_lines, reference) if a == r)
    accuracy = correct / max(len(reference), 1)

    assert accuracy >= 1.0, f"Accuracy too low: {accuracy} (Expected 1.0)"

    # 200,000 equations should be processed very quickly concurrently
    assert duration <= 1.5, f"Execution too slow: {duration}s (Expected <= 1.5s)"