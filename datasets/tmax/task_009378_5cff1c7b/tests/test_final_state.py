# test_final_state.py

import os
import re
import subprocess
import tempfile
import pytest

def get_joined_data():
    a_logs = {}
    with open('/home/user/service_A_logs.csv', 'r') as f:
        header = f.readline()
        for line in f:
            if not line.strip(): continue
            req, lat = line.strip().split(',')
            a_logs[int(req)] = float(lat)

    b_logs = {}
    with open('/home/user/service_B_logs.csv', 'r') as f:
        header = f.readline()
        for line in f:
            if not line.strip(): continue
            req, lat = line.strip().split(',')
            b_logs[int(req)] = float(lat)

    # Join and sort by req_id to ensure deterministic order
    joined = []
    for req in sorted(list(set(a_logs.keys()).intersection(set(b_logs.keys())))):
        joined.append(a_logs[req] + b_logs[req])
    return joined

def get_expected_ci():
    joined = get_joined_data()

    cpp_code = """
#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <iomanip>
#include <numeric>

int main() {
    std::vector<double> data = {
""" + ",".join(map(str, joined)) + """
    };
    int N = data.size();
    std::mt19937 gen(42);
    std::uniform_int_distribution<> dist(0, N - 1);

    std::vector<double> means(10000);
    for (int i = 0; i < 10000; ++i) {
        double sum = 0;
        for (int j = 0; j < N; ++j) {
            sum += data[dist(gen)];
        }
        means[i] = sum / N;
    }

    std::sort(means.begin(), means.end());
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Lower: " << means[250] << ", Upper: " << means[9750] << std::endl;
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "golden.cpp")
        bin_path = os.path.join(tmpdir, "golden")
        with open(src_path, "w") as f:
            f.write(cpp_code)

        subprocess.run(["g++", "-O3", src_path, "-o", bin_path], check=True)
        result = subprocess.run([bin_path], capture_output=True, text=True, check=True)
        return result.stdout.strip()

def test_bootstrap_cpp_exists():
    assert os.path.isfile("/home/user/bootstrap.cpp"), "/home/user/bootstrap.cpp is missing."

def test_ci_output_format_and_values():
    output_file = "/home/user/ci_output.txt"
    assert os.path.isfile(output_file), f"{output_file} is missing."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    match = re.match(r"^Lower:\s*([\d\.]+),\s*Upper:\s*([\d\.]+)$", content)
    assert match, f"Output format in {output_file} is incorrect. Expected 'Lower: [val], Upper: [val]', got '{content}'"

    student_lower = float(match.group(1))
    student_upper = float(match.group(2))

    expected_output = get_expected_ci()
    exp_match = re.match(r"^Lower:\s*([\d\.]+),\s*Upper:\s*([\d\.]+)$", expected_output)
    expected_lower = float(exp_match.group(1))
    expected_upper = float(exp_match.group(2))

    # We allow a small tolerance in case the student ordered the joined dataset differently
    # (e.g., by appearance in file A instead of sorted by req_id), which slightly changes the samples.
    assert abs(student_lower - expected_lower) < 0.5, f"Lower bound {student_lower} is too far from expected ~{expected_lower}"
    assert abs(student_upper - expected_upper) < 0.5, f"Upper bound {student_upper} is too far from expected ~{expected_upper}"