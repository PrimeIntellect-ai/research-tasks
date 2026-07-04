# test_final_state.py
import os
import subprocess
import pytest

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist. Did you save the final value?"

    with open(result_path, "r") as f:
        user_val_str = f.read().strip()

    try:
        user_val = float(user_val_str)
    except ValueError:
        pytest.fail(f"Could not parse '{user_val_str}' as a float. The result file should contain only the final value.")

    # Generate ground truth dynamically to avoid hardcoding and floating point architecture differences
    truth_cpp_code = """
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

double compute_dft_power(const vector<double>& sig, int start, int len) {
    double real_part = 0.0;
    double imag_part = 0.0;
    double freq = 0.05;
    for (int i = 0; i < len; ++i) {
        double angle = 2.0 * M_PI * freq * i;
        real_part += sig[start + i] * cos(angle);
        imag_part -= sig[start + i] * sin(angle);
    }
    return (real_part * real_part + imag_part * imag_part) / len;
}

int main() {
    vector<double> signal;
    ifstream infile("/home/user/signal.txt");
    double val;
    while (infile >> val) {
        signal.push_back(val);
    }

    int num_segments = 4;
    int seg_len = 250;

    double total_power = 0.0;
    // Sequential deterministic accumulation
    for (int i = 0; i < num_segments; ++i) {
        total_power += compute_dft_power(signal, i * seg_len, seg_len);
    }

    double k = 0.5;
    double learning_rate = 0.001;
    double target_concentration = 150.0;

    for (int step = 0; step < 1000; ++step) {
        double y = 0.0;
        double dt = 0.1;
        double t_end = 10.0;
        double y_grad = 0.0;

        for (double t = 0; t < t_end; t += dt) {
            y += (total_power - k * y) * dt;
            y_grad += (-y - k * y_grad) * dt; 
        }

        double error = y - target_concentration;
        double loss_grad = 2.0 * error * y_grad;
        double k_new = k - learning_rate * loss_grad;

        if (abs(k_new - k) < 1e-6) {
            k = k_new;
            break;
        }
        k = k_new;
    }

    cout << fixed << setprecision(6) << k << endl;
    return 0;
}
"""
    truth_cpp_path = "/tmp/truth_optimize_protein.cpp"
    truth_exe_path = "/tmp/truth_optimize_protein"

    with open(truth_cpp_path, "w") as f:
        f.write(truth_cpp_code)

    try:
        subprocess.run(["g++", "-O3", truth_cpp_path, "-o", truth_exe_path], check=True, capture_output=True)
        res = subprocess.run([truth_exe_path], capture_output=True, text=True, check=True)
        truth_val_str = res.stdout.strip()
    finally:
        if os.path.exists(truth_cpp_path):
            os.remove(truth_cpp_path)
        if os.path.exists(truth_exe_path):
            os.remove(truth_exe_path)

    assert user_val_str == truth_val_str, f"Expected deterministic value {truth_val_str}, but got {user_val_str}. Make sure you correctly implemented sequential accumulation."