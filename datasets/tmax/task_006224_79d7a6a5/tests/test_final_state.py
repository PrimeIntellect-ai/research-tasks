# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_analyze_c_exists():
    """Check that the user's C source code exists."""
    assert os.path.isfile("/home/user/analyze.c"), "The file /home/user/analyze.c does not exist."

def test_analysis_results_exists():
    """Check that the results file exists."""
    assert os.path.isfile("/home/user/analysis_results.txt"), "The file /home/user/analysis_results.txt does not exist."

def test_analysis_results_correctness():
    """Compile a reference C program to compute the exact expected results and compare."""
    reference_c_code = """
#include <stdio.h>
#include <stdlib.h>

int compare(const void *a, const void *b) {
    double da = *(double*)a;
    double db = *(double*)b;
    if (da < db) return -1;
    if (da > db) return 1;
    return 0;
}

int main() {
    FILE *f = fopen("/home/user/spectroscopy_data.csv", "r");
    if (!f) {
        return 1;
    }
    double data[100];
    int t;
    for (int i=0; i<100; i++) {
        if (fscanf(f, "%d,%lf", &t, &data[i]) != 2) break;
    }
    fclose(f);

    double S[100];
    for (int i=0; i<100; i++) S[i] = data[i];
    for (int i=2; i<98; i++) {
        S[i] = (data[i-2] + data[i-1] + data[i] + data[i+1] + data[i+2]) / 5.0;
    }

    double C[100];
    C[0] = 1.0;
    for (int i=1; i<100; i++) {
        C[i] = C[i-1] + 1.0 * (0.1 * C[i-1] * (1.0 - C[i-1] / 100.0));
    }

    double E[100];
    double mse = 0.0;
    for (int i=0; i<100; i++) {
        E[i] = (S[i] - C[i]) * (S[i] - C[i]);
        mse += E[i];
    }
    mse /= 100.0;

    srand(42);
    double bootstrap_means[1000];
    for (int b=0; b<1000; b++) {
        double sum = 0.0;
        for (int i=0; i<100; i++) {
            int idx = rand() % 100;
            sum += E[idx];
        }
        bootstrap_means[b] = sum / 100.0;
    }

    qsort(bootstrap_means, 1000, sizeof(double), compare);

    printf("MSE: %.4f\\n", mse);
    printf("CI_LOWER: %.4f\\n", bootstrap_means[24]);
    printf("CI_UPPER: %.4f\\n", bootstrap_means[974]);
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        ref_c_path = os.path.join(tmpdir, "ref.c")
        ref_bin_path = os.path.join(tmpdir, "ref")

        with open(ref_c_path, "w") as f:
            f.write(reference_c_code)

        compile_res = subprocess.run(["gcc", ref_c_path, "-o", ref_bin_path, "-lm"], capture_output=True)
        assert compile_res.returncode == 0, "Failed to compile reference C code."

        run_res = subprocess.run([ref_bin_path], capture_output=True, text=True)
        assert run_res.returncode == 0, "Failed to run reference C code."

        expected_output = run_res.stdout.strip().split('\n')

    expected_dict = {}
    for line in expected_output:
        if ':' in line:
            k, v = line.split(':')
            expected_dict[k.strip()] = float(v.strip())

    assert "MSE" in expected_dict, "Reference code failed to produce MSE."

    with open("/home/user/analysis_results.txt", "r") as f:
        actual_output = f.read().strip().split('\n')

    actual_dict = {}
    for line in actual_output:
        if ':' in line:
            k, v = line.split(':')
            actual_dict[k.strip()] = float(v.strip())

    for key in ["MSE", "CI_LOWER", "CI_UPPER"]:
        assert key in actual_dict, f"Missing {key} in /home/user/analysis_results.txt"
        expected_val = expected_dict[key]
        actual_val = actual_dict[key]
        assert abs(expected_val - actual_val) < 0.001, f"Expected {key} to be close to {expected_val:.4f}, but got {actual_val:.4f}."