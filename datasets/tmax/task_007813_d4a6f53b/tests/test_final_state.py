# test_final_state.py
import os
import subprocess
import pytest
import math

@pytest.fixture(scope="session")
def expected_results():
    ref_cpp = "/tmp/ref_mc_ode_sim.cpp"
    ref_out = "/tmp/ref_sim.out"

    cpp_code = """
#include <iostream>
#include <vector>
#include <random>
#include <cmath>
#include <omp.h>
#include <H5Cpp.h>
#include <fstream>
#include <iomanip>
#include <algorithm>

using namespace H5;

int main() {
    H5File file("/home/user/init_cond.h5", H5F_ACC_RDONLY);
    DataSet dataset = file.openDataSet("ic");
    DataSpace dataspace = dataset.getSpace();
    hsize_t dims[1];
    dataspace.getSimpleExtentDims(dims, NULL);
    int N = dims[0];

    std::vector<double> ic(N);
    dataset.read(ic.data(), PredType::NATIVE_DOUBLE);

    double dt = 0.01;
    int steps = 100;

    std::vector<double> final_vals(N);

    #pragma omp parallel for
    for (int i = 0; i < N; ++i) {
        std::mt19937 gen(1000 + i);
        std::normal_distribution<double> dist(0.0, 1.0);

        double y = ic[i];
        for (int step = 0; step < steps; ++step) {
            double dW = dist(gen) * std::sqrt(dt);
            y += -0.5 * y * dt + 0.1 * y * dW;
        }
        final_vals[i] = y;
    }

    double total_sum = 0.0;
    for (int i = 0; i < N; ++i) {
        total_sum += final_vals[i];
    }

    std::mt19937 boot_gen(42);
    std::uniform_int_distribution<int> boot_dist(0, N - 1);

    int B = 10000;
    std::vector<double> boot_means(B);
    for (int b = 0; b < B; ++b) {
        double b_sum = 0.0;
        for (int i = 0; i < N; ++i) {
            b_sum += final_vals[boot_dist(boot_gen)];
        }
        boot_means[b] = b_sum / N;
    }

    std::sort(boot_means.begin(), boot_means.end());

    double lower = boot_means[std::floor(B * 0.025)];
    double upper = boot_means[std::floor(B * 0.975)];

    std::cout << std::fixed << std::setprecision(6);
    std::cout << total_sum << "\\n" << lower << "\\n" << upper << "\\n";
    return 0;
}
"""
    with open(ref_cpp, "w") as f:
        f.write(cpp_code)

    compile_cmd = ["g++", "-O3", "-fopenmp", ref_cpp, "-o", ref_out, "-lhdf5_cpp", "-lhdf5"]
    try:
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile reference C++ code: {e.stderr.decode()}")

    try:
        res = subprocess.run([ref_out], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run reference C++ code: {e.stderr.decode()}")

    output = res.stdout.decode().strip().split('\n')
    assert len(output) == 3, "Reference code output format is incorrect."

    return {
        "sum": float(output[0]),
        "lower": float(output[1]),
        "upper": float(output[2])
    }

def test_executable_exists():
    assert os.path.exists("/home/user/sim.out"), "The executable /home/user/sim.out does not exist."
    assert os.access("/home/user/sim.out", os.X_OK), "The file /home/user/sim.out is not executable."

def test_results_file_exists():
    assert os.path.exists("/home/user/results.txt"), "The results file /home/user/results.txt does not exist."

def test_results_content(expected_results):
    with open("/home/user/results.txt", "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in /home/user/results.txt, found {len(lines)}."

    try:
        actual_sum = float(lines[0])
        actual_lower = float(lines[1])
        actual_upper = float(lines[2])
    except ValueError:
        pytest.fail("Could not parse the lines in /home/user/results.txt as floats.")

    # Check sum exactly (or very tight tolerance due to string conversion)
    assert math.isclose(actual_sum, expected_results["sum"], rel_tol=1e-6), \
        f"Expected sum {expected_results['sum']:.6f}, got {actual_sum:.6f}"

    # Check bounds
    assert math.isclose(actual_lower, expected_results["lower"], rel_tol=1e-4), \
        f"Expected lower bound {expected_results['lower']:.6f}, got {actual_lower:.6f}"

    assert math.isclose(actual_upper, expected_results["upper"], rel_tol=1e-4), \
        f"Expected upper bound {expected_results['upper']:.6f}, got {actual_upper:.6f}"