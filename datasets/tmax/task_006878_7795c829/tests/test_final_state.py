# test_final_state.py
import os
import subprocess
import pytest

def get_expected_result():
    c_code = """
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int compare_doubles(const void *a, const void *b) {
    double arg1 = *(const double *)a;
    double arg2 = *(const double *)b;
    if (arg1 < arg2) return -1;
    if (arg1 > arg2) return 1;
    return 0;
}

int main() {
    double data[1000];
    FILE *f = fopen("/home/user/spectrum.txt", "r");
    if (!f) return 1;
    for(int i=0; i<1000; i++) {
        fscanf(f, "%lf", &data[i]);
    }
    fclose(f);

    double Q[1000];
    double sum_Q = 0;
    for(int i=0; i<1000; i++) {
        Q[i] = exp(-i / 200.0);
        sum_Q += Q[i];
    }
    for(int i=0; i<1000; i++) Q[i] /= sum_Q;

    srand(42);
    double tvds[100];

    for(int b=0; b<100; b++) {
        double P[1000];
        double sum_P = 0;
        for(int i=0; i<1000; i++) {
            int idx = rand() % 1000;
            P[i] = data[idx];
            sum_P += P[i];
        }
        for(int i=0; i<1000; i++) P[i] /= sum_P;

        double tvd = 0;
        for(int i=0; i<1000; i++) {
            tvd += fabs(P[i] - Q[i]);
        }
        tvds[b] = tvd / 2.0;
    }

    qsort(tvds, 100, sizeof(double), compare_doubles);

    FILE *out = fopen("/tmp/expected_result.txt", "w");
    if (!out) return 1;
    fprintf(out, "CI: [%f, %f]\\n", tvds[4], tvds[94]);
    fclose(out);
    return 0;
}
"""
    with open("/tmp/ref_compare.c", "w") as f:
        f.write(c_code)

    subprocess.run(["gcc", "-O3", "/tmp/ref_compare.c", "-lm", "-o", "/tmp/ref_compare"], check=True)
    subprocess.run(["/tmp/ref_compare"], check=True)

    with open("/tmp/expected_result.txt", "r") as f:
        return f.read().strip()

def test_compare_spectra_c_exists():
    assert os.path.isfile("/home/user/compare_spectra.c"), "/home/user/compare_spectra.c does not exist."

def test_result_txt_exists():
    assert os.path.isfile("/home/user/result.txt"), "/home/user/result.txt does not exist."

def test_result_txt_content():
    expected_str = get_expected_result()

    with open("/home/user/result.txt", "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Contents of /home/user/result.txt do not match exactly. Expected: '{expected_str}', Got: '{actual_str}'"