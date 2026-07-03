# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_mc_motif_cpp_exists():
    """Test that the C++ source file exists."""
    cpp_path = "/home/user/mc_motif.cpp"
    assert os.path.exists(cpp_path), f"File {cpp_path} does not exist."
    assert os.path.isfile(cpp_path), f"Path {cpp_path} is not a file."

def test_makefile_exists():
    """Test that the Makefile exists."""
    makefile_path = "/home/user/Makefile"
    assert os.path.exists(makefile_path), f"File {makefile_path} does not exist."
    assert os.path.isfile(makefile_path), f"Path {makefile_path} is not a file."

def test_result_txt_is_correct():
    """Test that result.txt exists and contains the correct computed output."""
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"File {result_path} does not exist."
    assert os.path.isfile(result_path), f"Path {result_path} is not a file."

    # Compute the expected output using a known-good C++ implementation
    # to ensure strict alignment with the C++ std::mt19937 RNG sequence.
    truth_cpp = """
#include <iostream>
#include <string>
#include <random>
#include <iomanip>

int main() {
    std::string ref = "ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTGATTACAGATTACAGATTACAGATTACAGATTACAGATTACCCGGGAAATTTCCCGGGAAATTTCCCGGGAAATTTCCCGGATTACAGATTACAGATTACAGATTACAGATTACAGATTAACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT";
    std::string motif = "GATTACA";
    uint32_t mut_rate = 15;
    uint32_t iters = 10000;
    uint32_t seed = 42;

    std::mt19937 rng(seed);
    long long total_motifs = 0;

    for (uint32_t i = 0; i < iters; ++i) {
        std::string mutated = ref;
        for (size_t j = 0; j < mutated.size(); ++j) {
            uint32_t r1 = rng();
            if (r1 % 100 < mut_rate) {
                uint32_t r2 = rng();
                char c = mutated[j];
                char pool[3];
                int idx = 0;
                if (c != 'A') pool[idx++] = 'A';
                if (c != 'C') pool[idx++] = 'C';
                if (c != 'G') pool[idx++] = 'G';
                if (c != 'T') pool[idx++] = 'T';
                mutated[j] = pool[r2 % 3];
            }
        }

        size_t pos = 0;
        while ((pos = mutated.find(motif, pos)) != std::string::npos) {
            total_motifs++;
            pos++;
        }
    }

    std::cout << std::fixed << std::setprecision(4) << (double)total_motifs / iters << std::endl;
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "truth.cpp")
        exe_path = os.path.join(tmpdir, "truth")

        with open(src_path, "w") as f:
            f.write(truth_cpp)

        compile_proc = subprocess.run(["g++", "-O3", src_path, "-o", exe_path], capture_output=True)
        assert compile_proc.returncode == 0, "Failed to compile truth C++ code."

        run_proc = subprocess.run([exe_path], capture_output=True, text=True)
        assert run_proc.returncode == 0, "Failed to run truth C++ code."
        expected_output = run_proc.stdout.strip()

    with open(result_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"result.txt content is incorrect. Expected '{expected_output}', got '{actual_output}'."