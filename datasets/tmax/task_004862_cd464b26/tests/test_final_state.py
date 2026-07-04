# test_final_state.py
import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = '/opt/oracle/processor_oracle.py'
TARGET_PATH = '/home/user/processor'

def generate_csv():
    num_rows = random.randint(5, 50)
    lines = []
    for _ in range(num_rows):
        num_words = random.randint(1, 20)
        words = [''.join(random.choices(string.ascii_letters, k=random.randint(1, 10))) for _ in range(num_words)]
        text_data = ' '.join(words)
        float_x = f"{random.uniform(0.1, 0.9):.3f}"
        float_y = f"{random.uniform(0.1, 0.9):.3f}"
        lines.append(f"{text_data},{float_x},{float_y}")
    return '\n'.join(lines)

def test_fuzz_equivalence():
    assert os.path.exists(TARGET_PATH), f"Target executable not found at {TARGET_PATH}"
    assert os.access(TARGET_PATH, os.X_OK), f"Target {TARGET_PATH} is not executable"

    # Ensure oracle exists
    if not os.path.exists(ORACLE_PATH):
        os.makedirs(os.path.dirname(ORACLE_PATH), exist_ok=True)
        with open(ORACLE_PATH, 'w') as f:
            f.write("""#!/usr/bin/env python3
import sys
import math

PRIOR = 0.35

def main():
    lines = sys.stdin.read().strip().split('\\n')
    if not lines or lines == ['']:
        return

    token_counts = []
    xs = []
    ys = []

    for line in lines:
        parts = line.split(',', 2)
        if len(parts) < 3: continue
        text, x_str, y_str = parts

        tokens = text.split()
        token_counts.append(len(tokens))
        xs.append(float(x_str))
        ys.append(float(y_str))

        print(f"{len(tokens)},{float(x_str):.4f},{float(y_str):.4f}")

    print("")

    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n

    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / n

    prod_x = 1.0
    prod_y = 1.0
    for x in xs: prod_x *= x
    for y in ys: prod_y *= y

    numerator = PRIOR * prod_x
    denominator = numerator + (1.0 - PRIOR) * prod_y

    posterior = 0.0
    if denominator > 0:
        posterior = numerator / denominator

    print(f"COVARIANCE: {cov:.4f}")
    print(f"POSTERIOR: {posterior:.4f}")

if __name__ == '__main__':
    main()
""")
        os.chmod(ORACLE_PATH, 0o755)

    random.seed(42)

    for i in range(100):
        csv_input = generate_csv()

        oracle_proc = subprocess.run([ORACLE_PATH], input=csv_input, text=True, capture_output=True)
        target_proc = subprocess.run([TARGET_PATH], input=csv_input, text=True, capture_output=True)

        assert target_proc.returncode == 0, f"Target failed on run {i}:\n{target_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip()
        target_out = target_proc.stdout.strip()

        if oracle_out != target_out:
            pytest.fail(f"Mismatch on run {i}.\nInput:\n{csv_input}\n\nExpected Output:\n{oracle_out}\n\nActual Output:\n{target_out}")