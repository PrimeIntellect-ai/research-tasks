# test_final_state.py

import os
import subprocess
import pytest

GOLDEN_C_CODE = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct {
    double x, y;
} Point;

int main() {
    FILE *f = fopen("/home/user/dataset.csv", "r");
    if (!f) return 1;
    char line[256];
    Point points[100];
    int count = 0;

    fgets(line, sizeof(line), f); // skip header
    while (fgets(line, sizeof(line), f)) {
        if (strstr(line, "?") != NULL) continue;
        sscanf(line, "%lf,%lf", &points[count].x, &points[count].y);
        count++;
    }
    fclose(f);

    double sum_x = 0, sum_y = 0;
    for (int i = 0; i < count; i++) {
        sum_x += points[i].x;
        sum_y += points[i].y;
    }
    double mean_x = sum_x / count;
    double mean_y = sum_y / count;

    double dists[100];
    double sum_dist = 0;
    for (int i = 0; i < count; i++) {
        dists[i] = sqrt(pow(points[i].x - mean_x, 2) + pow(points[i].y - mean_y, 2));
        sum_dist += dists[i];
    }
    double mean_dist = sum_dist / count;

    double sum_sq_diff = 0;
    for (int i = 0; i < count; i++) {
        sum_sq_diff += pow(dists[i] - mean_dist, 2);
    }
    double std_dist = sqrt(sum_sq_diff / count);

    Point cleaned[100];
    int clean_count = 0;
    for (int i = 0; i < count; i++) {
        if (dists[i] <= mean_dist + 2.0 * std_dist) {
            cleaned[clean_count++] = points[i];
        }
    }

    srand(42);
    double sum_corr = 0;
    int N = clean_count;

    for (int iter = 0; iter < 10000; iter++) {
        Point sample[100];
        double sx = 0, sy = 0;
        for (int i = 0; i < N; i++) {
            int idx = rand() % N;
            sample[i] = cleaned[idx];
            sx += sample[i].x;
            sy += sample[i].y;
        }
        double mx = sx / N, my = sy / N;

        double num = 0, den_x = 0, den_y = 0;
        for (int i = 0; i < N; i++) {
            double dx = sample[i].x - mx;
            double dy = sample[i].y - my;
            num += dx * dy;
            den_x += dx * dx;
            den_y += dy * dy;
        }

        double corr = 0;
        if (den_x > 0 && den_y > 0) {
            corr = num / sqrt(den_x * den_y);
        }
        sum_corr += corr;
    }

    printf("%.4f\\n", sum_corr / 10000.0);
    return 0;
}
"""

def test_c_program_exists():
    assert os.path.isfile("/home/user/prepare_data.c"), "The required C program /home/user/prepare_data.c is missing."

def test_robust_corr_exists():
    assert os.path.isfile("/home/user/robust_corr.txt"), "The output file /home/user/robust_corr.txt is missing."

def test_robust_corr_value(tmp_path):
    c_file = tmp_path / "golden.c"
    c_file.write_text(GOLDEN_C_CODE)

    exe_file = tmp_path / "golden"
    compile_proc = subprocess.run(
        ["gcc", str(c_file), "-o", str(exe_file), "-lm"], 
        capture_output=True
    )
    assert compile_proc.returncode == 0, f"Failed to compile golden C code in test: {compile_proc.stderr.decode()}"

    run_proc = subprocess.run([str(exe_file)], capture_output=True, text=True)
    assert run_proc.returncode == 0, "Failed to run golden C code in test."

    expected_value = run_proc.stdout.strip()

    with open("/home/user/robust_corr.txt", "r") as f:
        actual_value = f.read().strip()

    assert actual_value == expected_value, f"Expected correlation {expected_value}, but got {actual_value} in /home/user/robust_corr.txt"