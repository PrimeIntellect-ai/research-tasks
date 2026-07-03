# test_final_state.py
import os
import math

def test_bottleneck_txt():
    bottleneck_path = "/home/user/bottleneck.txt"
    assert os.path.exists(bottleneck_path), f"File {bottleneck_path} does not exist."
    with open(bottleneck_path, "r") as f:
        content = f.read().strip()
    assert "dense_lu_solve" in content, f"Expected 'dense_lu_solve' in bottleneck.txt, got: {content}"

def test_solution_txt():
    solution_path = "/home/user/solution.txt"
    assert os.path.exists(solution_path), f"File {solution_path} does not exist."
    with open(solution_path, "r") as f:
        content = f.read().strip()

    try:
        alpha_val = float(content)
    except ValueError:
        assert False, f"Could not parse float from solution.txt: {content}"

    expected_alpha = 0.027878
    assert math.isclose(alpha_val, expected_alpha, rel_tol=1e-2, abs_tol=1e-3), \
        f"Expected alpha value close to {expected_alpha}, got {alpha_val}"

def test_heat_opt_c_modified():
    source_path = "/home/user/heat_opt.c"
    assert os.path.exists(source_path), f"File {source_path} does not exist."
    with open(source_path, "r") as f:
        content = f.read()

    # The student was supposed to replace the $O(N^3)$ dense_lu_solve with a Thomas algorithm.
    # While they might keep the function name, the implementation should no longer have the triply nested loops.
    # We can check if the file still contains the exact original LU decomposition loops.
    original_loop_snippet = "for (int j = 0; j < i; j++)"
    count_original_loops = content.count(original_loop_snippet)
    # The original file has it 3 times. If optimized, it should be fewer or gone.
    assert count_original_loops < 3, "It appears the dense LU decomposition is still present in heat_opt.c."