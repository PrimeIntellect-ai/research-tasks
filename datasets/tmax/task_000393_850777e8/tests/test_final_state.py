# test_final_state.py
import os
import subprocess

def test_regression_result_deterministic():
    result_file = "/home/user/regression_result.txt"
    assert os.path.isfile(result_file), f"Expected output file {result_file} does not exist."

    with open(result_file, "r") as f:
        actual_output = f.read().strip()

    golden_cpp = """#include <iostream>
#include <vector>
#include <thread>
#include <cmath>
#include <iomanip>

const int N = 1000;
const int NUM_THREADS = 10;

struct BlockData {
    double x, y, xy, xx;
};
std::vector<BlockData> blocks(NUM_THREADS);

void process_block(int thread_id) {
    int rows_per_thread = N / NUM_THREADS;
    int start_row = thread_id * rows_per_thread;
    int end_row = start_row + rows_per_thread;

    double loc_x = 0, loc_y = 0, loc_xy = 0, loc_xx = 0;
    for(int i = start_row; i < end_row; ++i) {
        for(int j = 0; j < N; ++j) {
            double x = i * N + j;
            double y = std::sin(x * 0.001) + x * 0.005;
            loc_x += x;
            loc_y += y;
            loc_xy += x * y;
            loc_xx += x * x;
        }
    }

    blocks[thread_id] = {loc_x, loc_y, loc_xy, loc_xx};
}

int main() {
    std::vector<std::thread> threads;
    for(int i = 0; i < NUM_THREADS; ++i) {
        threads.push_back(std::thread(process_block, i));
    }
    for(auto& t : threads) {
        t.join();
    }

    double sum_x = 0, sum_y = 0, sum_xy = 0, sum_xx = 0;
    for(int i = 0; i < NUM_THREADS; ++i) {
        sum_x += blocks[i].x;
        sum_y += blocks[i].y;
        sum_xy += blocks[i].xy;
        sum_xx += blocks[i].xx;
    }

    double n_total = N * N;
    double slope = (n_total * sum_xy - sum_x * sum_y) / (n_total * sum_xx - sum_x * sum_x);
    double intercept = (sum_y - slope * sum_x) / n_total;

    std::cout << std::fixed << std::setprecision(9) << slope << "," << intercept << std::endl;
    return 0;
}
"""
    golden_src = "/tmp/golden_gen_test.cpp"
    golden_bin = "/tmp/golden_gen_test"
    with open(golden_src, "w") as f:
        f.write(golden_cpp)

    try:
        subprocess.run(["g++", "-O3", "-pthread", golden_src, "-o", golden_bin], check=True, capture_output=True)
        comp_proc = subprocess.run([golden_bin], capture_output=True, text=True, check=True)
        expected_output = comp_proc.stdout.strip()
    finally:
        if os.path.exists(golden_src):
            os.remove(golden_src)
        if os.path.exists(golden_bin):
            os.remove(golden_bin)

    assert actual_output == expected_output, (
        f"Result '{actual_output}' does not match the expected deterministic result '{expected_output}'. "
        "Ensure sequential accumulation by thread_id is implemented correctly."
    )

def test_code_modified_no_mutex():
    cpp_file = "/home/user/data_gen.cpp"
    assert os.path.isfile(cpp_file), f"File {cpp_file} does not exist."
    with open(cpp_file, "r") as f:
        content = f.read()

    assert "std::lock_guard<std::mutex>" not in content and "mtx.lock()" not in content, (
        "The code still uses a mutex lock, which violates the requirement to use a deterministic sequential reduction."
    )