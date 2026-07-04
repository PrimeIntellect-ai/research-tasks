# test_final_state.py
import os
import subprocess
import tempfile
import pytest

def test_source_code_exists():
    assert os.path.isfile("/home/user/mc_spectroscopy.c"), "Source code /home/user/mc_spectroscopy.c is missing."

def test_log_exists():
    assert os.path.isfile("/home/user/mc_regression.log"), "Log file /home/user/mc_regression.log is missing."

def test_kl_divergence_value():
    reference_c_code = """
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {
    FILE *f = fopen("/home/user/baseline.txt", "r");
    if (!f) return 1;
    double Q[100];
    double sum_Q = 0;
    for(int i=0; i<100; i++) {
        fscanf(f, "%lf", &Q[i]);
        sum_Q += Q[i];
    }
    fclose(f);

    for(int i=0; i<100; i++) Q[i] /= sum_Q;

    srand(42);
    int hits[100] = {0};
    for(int i=0; i<10000; i++) {
        double r = (double)rand() / RAND_MAX;
        double cumulative = 0;
        for(int j=0; j<100; j++) {
            cumulative += Q[j];
            if(r <= cumulative) {
                hits[j]++;
                break;
            }
        }
    }

    double P[100];
    for(int i=0; i<100; i++) {
        P[i] = (double)hits[i] / 10000.0;
    }

    double sum_P_new = 0, sum_Q_new = 0;
    for(int i=0; i<100; i++) {
        P[i] += 1e-6;
        Q[i] += 1e-6;
        sum_P_new += P[i];
        sum_Q_new += Q[i];
    }
    for(int i=0; i<100; i++) {
        P[i] /= sum_P_new;
        Q[i] /= sum_Q_new;
    }

    double kl = 0;
    for(int i=0; i<100; i++) {
        kl += P[i] * log(P[i] / Q[i]);
    }

    printf("KL: %.6f\\n", kl);
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "ref.c")
        bin_path = os.path.join(tmpdir, "ref_bin")

        with open(src_path, "w") as f:
            f.write(reference_c_code)

        compile_res = subprocess.run(["gcc", src_path, "-o", bin_path, "-lm"], capture_output=True)
        assert compile_res.returncode == 0, f"Failed to compile reference C code: {compile_res.stderr.decode()}"

        run_res = subprocess.run([bin_path], capture_output=True, text=True)
        assert run_res.returncode == 0, "Failed to execute reference binary."

        expected_output = run_res.stdout.strip()

    with open("/home/user/mc_regression.log", "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Log file content mismatch. Expected '{expected_output}', got '{actual_output}'."