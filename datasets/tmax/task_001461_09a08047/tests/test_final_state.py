# test_final_state.py
import os

def test_benchmark_results():
    path = "/home/user/benchmark_results.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the benchmark and redirect standard output?"
    with open(path, "r") as f:
        content = f.read()

    # 1234 * 5678 = 7006652
    # 1234 + 5678 = 6912
    # 7006652 ^ 6912 = 7001476
    expected_result = "SUCCESS: 7001476"
    assert expected_result in content, f"Expected '{expected_result}' in {path}. Check your C translation and build."

def test_fast_compute_assembly():
    path = "/home/user/fast_compute.s"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run objdump and save the output?"
    with open(path, "r") as f:
        content = f.read()
    assert "<fast_compute>:" in content, f"Expected to find '<fast_compute>:' in {path}. Ensure you disassembled libmathops.so correctly."

def test_cmakelists_linked():
    path = "/home/user/pr_review/CMakeLists.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "target_link_libraries" in content, f"Expected 'target_link_libraries' to be used in {path} to link the shared library."
    assert "bench" in content and "mathops" in content, "CMakeLists.txt must reference both 'bench' and 'mathops'."