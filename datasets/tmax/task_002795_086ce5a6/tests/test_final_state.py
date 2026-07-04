# test_final_state.py
import os
import subprocess
import tempfile
import pytest

def test_training_data_exists():
    """Verify that the training_data.txt file exists."""
    assert os.path.isfile("/home/user/training_data.txt"), "/home/user/training_data.txt does not exist."

def test_training_data_contents():
    """Verify that the training data contains the correct deterministic results."""
    # Write a reference implementation in C++ to compute the exact expected values
    # This ensures we use the exact same libc rand() and floating point semantics
    ref_cpp_code = """
#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <iomanip>

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    int seed = std::atoi(argv[1]);
    std::srand(seed);

    int N = 10000;
    std::vector<double> data(N);
    for (int i = 0; i < N; ++i) {
        data[i] = (std::rand() % 1000) / 100.0;
    }

    double x = 0.0;
    double learning_rate = 0.01;

    for (int iter = 0; iter < 5000; ++iter) {
        double gradient = 0.0;
        for (int i = 0; i < N; ++i) {
            gradient += (x - data[i]);
        }
        gradient /= N;

        if (std::abs(gradient) <= 1e-5) {
            break;
        }

        x = x - learning_rate * gradient;
    }

    std::cout << std::fixed << std::setprecision(6) << x << std::endl;
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        ref_cpp_path = os.path.join(tmpdir, "ref_sim.cpp")
        ref_bin_path = os.path.join(tmpdir, "ref_sim")

        with open(ref_cpp_path, "w") as f:
            f.write(ref_cpp_code)

        # Compile reference implementation
        compile_result = subprocess.run(
            ["g++", "-O2", ref_cpp_path, "-o", ref_bin_path],
            capture_output=True, text=True
        )
        assert compile_result.returncode == 0, f"Failed to compile reference C++ code: {compile_result.stderr}"

        expected_outputs = []
        seeds = [10, 20, 30, 40, 50]
        for seed in seeds:
            run_result = subprocess.run(
                [ref_bin_path, str(seed)],
                capture_output=True, text=True
            )
            assert run_result.returncode == 0, f"Reference binary failed for seed {seed}"
            expected_outputs.append(run_result.stdout.strip())

    # Read the agent's output
    with open("/home/user/training_data.txt", "r") as f:
        agent_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(agent_lines) == len(seeds), f"Expected {len(seeds)} lines in training_data.txt, found {len(agent_lines)}"

    for i, (expected, actual) in enumerate(zip(expected_outputs, agent_lines)):
        assert actual == expected, f"Output mismatch for seed {seeds[i]}: expected {expected}, got {actual}"

def test_sim_cpp_modifications():
    """Verify that the simulation code was modified correctly."""
    sim_cpp_path = "/home/user/sim.cpp"
    assert os.path.isfile(sim_cpp_path), f"The file {sim_cpp_path} does not exist."

    with open(sim_cpp_path, 'r') as f:
        content = f.read()

    assert "#pragma omp atomic" not in content, "The non-deterministic '#pragma omp atomic' directive was not removed."
    assert "iter < 100" not in content, "The fixed iteration loop condition 'iter < 100' was not removed."
    assert "1e-5" in content or "0.00001" in content, "Convergence threshold 1e-5 is missing from the code."
    assert "5000" in content, "Maximum iteration bound of 5000 is missing from the code."