# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def get_expected_output():
    c_code = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

float integrate_spectral_energy(float* energy_array, int n) {
    float sum = 0.0f;
    float c = 0.0f;
    for(int i=0; i<n; i++) {
        float y = energy_array[i] - c;
        float t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    return sum;
}

void generate_spectrum(const char* primer, float* out_array, int n) {
    float base_val = 0.0f;
    for(int i=0; i<8; i++) {
        base_val += (float)(primer[i] * (i+1));
    }

    for(int i = 0; i < n; i++) {
        if (i % 2 == 0) out_array[i] = 10000.0f;
        else out_array[i] = -10000.0f + (base_val * 0.0001f);
    }
}

int main(int argc, char** argv) {
    int seed = 42;
    srand(seed);

    char current_primer[9] = "AAAAAAAA";
    float best_score = -1e9;
    char best_primer[9] = "AAAAAAAA";

    int n_points = 50000;
    float* spectrum = malloc(n_points * sizeof(float));

    for(int step = 0; step < 1000; step++) {
        char proposed_primer[9];
        strcpy(proposed_primer, current_primer);

        int mut_idx = rand() % 8;
        char bases[] = "ATCG";
        proposed_primer[mut_idx] = bases[rand() % 4];

        generate_spectrum(proposed_primer, spectrum, n_points);
        float score = integrate_spectral_energy(spectrum, n_points);

        if(score > best_score) {
            best_score = score;
            strcpy(best_primer, proposed_primer);
            strcpy(current_primer, proposed_primer);
        }
    }

    printf("Best Primer: %s\\n", best_primer);
    printf("Score: %.4f\\n", best_score);

    free(spectrum);
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "test.c")
        exe = os.path.join(td, "test_exe")
        with open(src, "w") as f:
            f.write(c_code)

        subprocess.run(["gcc", src, "-o", exe, "-lm"], check=True)
        result = subprocess.run([exe], capture_output=True, text=True, check=True)
        return result.stdout.strip()

def test_result_log_exists_and_correct():
    result_path = "/home/user/result.log"
    assert os.path.isfile(result_path), f"Missing result file: {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected_output = get_expected_output()

    assert expected_output in content, (
        f"The content of {result_path} does not match the expected output of the Kahan-summed MCMC sampler.\n"
        f"Expected to find:\n{expected_output}\n"
        f"But found:\n{content}"
    )

def test_mcmc_primer_c_uses_kahan():
    c_file_path = "/home/user/mcmc_primer.c"
    assert os.path.isfile(c_file_path), f"Missing C source file: {c_file_path}"

    with open(c_file_path, "r") as f:
        content = f.read()

    # Extract the integrate_spectral_energy function
    start_idx = content.find("float integrate_spectral_energy")
    assert start_idx != -1, "Could not find integrate_spectral_energy function"

    end_idx = content.find("}", start_idx)
    func_body = content[start_idx:end_idx]

    # Check for characteristics of Kahan summation:
    # It requires at least 4 operations/variables inside the loop to compute the compensated sum
    assert "-" in func_body, "Kahan summation requires subtraction to compute the compensation error."
    assert "+" in func_body, "Kahan summation requires addition."

    # Count assignments in the loop roughly
    assignments = func_body.count("=")
    assert assignments >= 4, "Kahan summation requires multiple assignments inside the loop to track sum, error, and temporary values."