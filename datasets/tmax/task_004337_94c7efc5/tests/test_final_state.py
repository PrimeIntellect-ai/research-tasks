# test_final_state.py

import os
import re
import random
import subprocess
import urllib.request
import urllib.parse
import pytest

def generate_expression(max_len=256):
    # Simple recursive generator for math expressions
    def gen_expr(depth):
        if depth > 5 or random.random() < 0.3:
            return str(random.randint(1, 999))

        op = random.choice(['+', '-', '*', '/'])
        left = gen_expr(depth + 1)
        right = gen_expr(depth + 1)

        # Avoid division by zero
        if op == '/' and right == '0':
            right = str(random.randint(1, 999))

        fmt = random.choice(["{0}{1}{2}", "({0}{1}{2})"])
        return fmt.format(left, op, right)

    while True:
        expr = gen_expr(0)
        if 3 <= len(expr) <= max_len:
            # Ensure no division by zero in the generated string
            try:
                eval(expr)
                return expr
            except ZeroDivisionError:
                continue
            except Exception:
                continue

def test_fuzz_equivalence():
    agent_script = "/home/user/run_eval.sh"
    oracle_bin = "/app/bin/math_oracle_v3"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable"

    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable"

    random.seed(42)
    # Using 1000 iterations to ensure it completes within reasonable time limits
    # while still providing strong fuzzing guarantees.
    N = 1000

    for _ in range(N):
        expr = generate_expression()

        oracle_proc = subprocess.run([oracle_bin, expr], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_script, expr], capture_output=True, text=True)

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input: '{expr}'\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )

def test_nginx_routing():
    expr = "1+1"
    url = f"http://localhost/api/eval?expr={urllib.parse.quote(expr)}"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        res = req.read().decode('utf-8').strip()
        assert res == "2", f"Expected '2' from Nginx for 1+1, got '{res}'"
    except Exception as e:
        pytest.fail(f"Nginx routing check failed: {e}")

def test_benchmark_and_test_scripts():
    benchmark_script = "/home/user/math_engine/benchmark.py"
    test_script = "/home/user/math_engine/test_eval.py"

    assert os.path.isfile(benchmark_script), f"Benchmark script not found at {benchmark_script}"
    assert os.path.isfile(test_script), f"Test script not found at {test_script}"

    # Check execution success
    bench_proc = subprocess.run(["python3", benchmark_script], capture_output=True)
    assert bench_proc.returncode == 0, f"Benchmark script failed: {bench_proc.stderr.decode()}"

    test_proc = subprocess.run(["python3", test_script], capture_output=True)
    # Could be run with pytest or python3 directly
    assert test_proc.returncode == 0, f"Test script failed: {test_proc.stderr.decode()}"

def test_extracted_grammar():
    grammar_file = "/home/user/extracted_grammar.txt"
    assert os.path.isfile(grammar_file), f"Extracted grammar file not found at {grammar_file}"

    with open(grammar_file, "r") as f:
        content = f.read()

    pattern = re.compile(r"EXPR\s*::=\s*TERM.*NUMBER\s*::=\s*\[0-9\]\+", re.IGNORECASE | re.DOTALL)
    assert pattern.search(content), "Extracted grammar does not match the expected EBNF rules"