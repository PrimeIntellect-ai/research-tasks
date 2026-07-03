# test_final_state.py
import os
import re
import subprocess

def get_expected_ci():
    """
    Compiles and runs a small C program to get the exact reproducible
    bootstrap CI bounds using the system's rand() implementation.
    """
    c_code = """
    #include <stdio.h>
    #include <stdlib.h>

    int compare_doubles(const void *a, const void *b) {
        double diff = *(double*)a - *(double*)b;
        if (diff < 0) return -1;
        if (diff > 0) return 1;
        return 0;
    }

    int main() {
        double vals[] = {10.5, 11.2, 10.8, 11.5, 10.1};
        int N = 5;
        double means[10000];
        srand(42);
        for (int i = 0; i < 10000; i++) {
            double sum = 0;
            for (int j = 0; j < N; j++) {
                int idx = rand() % N;
                sum += vals[idx];
            }
            means[i] = sum / N;
        }
        qsort(means, 10000, sizeof(double), compare_doubles);
        printf("%.4f\\n%.4f\\n", means[250], means[9750]);
        return 0;
    }
    """
    c_file = "/tmp/test_calc_ci.c"
    exe_file = "/tmp/test_calc_ci"

    with open(c_file, "w") as f:
        f.write(c_code)

    subprocess.run(["gcc", c_file, "-o", exe_file], check=True)
    res = subprocess.run([exe_file], capture_output=True, text=True, check=True)

    lines = res.stdout.strip().split('\n')
    return lines[0], lines[1]

def test_report_exists_and_content():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Output file {report_path} was not created."

    with open(report_path, 'r') as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split('\n') if line.strip()]
    assert len(lines) == 4, f"Expected exactly 4 lines in {report_path}, found {len(lines)}."

    # Verify exact means based on the provided valid data
    assert lines[0] == "Mean 1: 10.8200", f"Expected 'Mean 1: 10.8200', got '{lines[0]}'"
    assert lines[1] == "Mean 2: 20.7500", f"Expected 'Mean 2: 20.7500', got '{lines[1]}'"

    # Verify CI bounds
    expected_lower, expected_upper = get_expected_ci()

    assert lines[2] == f"CI 1 Lower: {expected_lower}", f"Expected 'CI 1 Lower: {expected_lower}', got '{lines[2]}'"
    assert lines[3] == f"CI 1 Upper: {expected_upper}", f"Expected 'CI 1 Upper: {expected_upper}', got '{lines[3]}'"