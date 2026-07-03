# test_final_state.py

import os
import subprocess
import re
import math

def test_bad_commit_identified():
    bad_commit_file = '/home/user/bad_commit.txt'
    assert os.path.isfile(bad_commit_file), f"Expected {bad_commit_file} to exist."

    with open(bad_commit_file, 'r') as f:
        student_hash = f.read().strip()

    # Get the actual bad commit hash from git
    try:
        expected_hash = subprocess.check_output(
            ['git', 'log', '--grep=Optimize solver with pthreads', '--format=%H'],
            cwd='/home/user/project', text=True
        ).strip()
    except subprocess.CalledProcessError:
        assert False, "Failed to run git log to find the bad commit."

    assert expected_hash, "Could not find the bad commit in the git history."
    assert student_hash == expected_hash, f"Incorrect bad commit hash. Expected {expected_hash}, got {student_hash}"

def test_pipeline_output_correct():
    output_file = '/home/user/pipeline_output.txt'
    assert os.path.isfile(output_file), f"Expected {output_file} to exist."

    with open(output_file, 'r') as f:
        content = f.read()

    assert "Failed to converge" not in content, "Pipeline output still shows convergence failures."

    # Calculate expected sums
    def calc_sum(filepath):
        total = 0.0
        with open(filepath, 'r') as f:
            for line in f:
                val = float(line.strip())
                # Emulate the Newton's method in the C code
                x = val
                for _ in range(10000):
                    delta = (x * x - val) / (2 * x)
                    if abs(delta) < 1e-5:
                        break
                    x -= delta
                total += x
        return total

    dataset1_sum = calc_sum('/home/user/project/data/dataset 1.txt')
    dataset2_sum = calc_sum('/home/user/project/data/dataset 2.txt')

    # The C code formats as %.4f
    expected_1 = f"File: data/dataset 1.txt | Sum of roots: {dataset1_sum:.4f}"
    expected_2 = f"File: data/dataset 2.txt | Sum of roots: {dataset2_sum:.4f}"

    # Check if the output contains the expected lines
    assert expected_1 in content, f"Output missing or incorrect for dataset 1. Expected: '{expected_1}'"
    assert expected_2 in content, f"Output missing or incorrect for dataset 2. Expected: '{expected_2}'"

def test_solver_c_fixed():
    solver_path = '/home/user/project/solver.c'
    assert os.path.isfile(solver_path), f"Expected {solver_path} to exist."

    with open(solver_path, 'r') as f:
        content = f.read()

    # Check that multithreading is still used
    assert "pthread_create" in content, "solver.c must remain multithreaded (do not revert to single-threaded)."

    # Check that global delta is removed or moved
    # A simple regex to see if `double delta;` is at the global scope.
    # We can check if `double delta;` is declared before `void* worker`
    worker_idx = content.find('void* worker')
    if worker_idx != -1:
        global_area = content[:worker_idx]
        assert "double delta;" not in global_area, "The race condition is not fixed: 'delta' is still a global variable."

    # Also verify it compiles and runs without race conditions (implied by pipeline output test, but we can check code)
    assert re.search(r'double\s+delta\s*=', content[worker_idx:]) or re.search(r'double\s+delta\s*;\s*delta\s*=', content[worker_idx:]), "delta must be declared locally inside the worker thread."

def test_run_pipeline_sh_fixed():
    script_path = '/home/user/project/run_pipeline.sh'
    assert os.path.isfile(script_path), f"Expected {script_path} to exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "$(ls" not in content, "run_pipeline.sh still uses $(ls ...), which breaks on spaces."
    assert "dataset 1.txt" not in content, "run_pipeline.sh should iterate over files, not hardcode them."

    # It should iterate over data/* or use find/xargs properly
    valid_patterns = [r'for\s+\w+\s+in\s+data/\*', r'find\s+data', r'ls\s+data/\*\s*\|\s*while']
    has_valid_loop = any(re.search(p, content) for p in valid_patterns)
    assert has_valid_loop or '"$@"' in content or 'data/' in content, "run_pipeline.sh does not seem to iterate over data/ directory correctly."