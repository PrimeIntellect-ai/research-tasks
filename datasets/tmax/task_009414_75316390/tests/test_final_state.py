# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def get_expected_volume():
    cpp_code = """
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <omp.h>
#include <random>
#include <iomanip>

struct Atom { float x, y, z, r; };

int main() {
    std::vector<Atom> atoms;
    std::ifstream in("/home/user/protein.pdb");
    std::string line;
    while(std::getline(in, line)) {
        if(line.substr(0,4) == "ATOM") {
            float x = std::stof(line.substr(30, 8));
            float y = std::stof(line.substr(38, 8));
            float z = std::stof(line.substr(46, 8));
            atoms.push_back({x, y, z, 1.5f});
        }
    }

    int num_samples = 1000000;
    float box_size = 20.0f;
    float box_volume = box_size * box_size * box_size;

    int hits = 0;
    float vol_per_sample = box_volume / num_samples;

    #pragma omp parallel for reduction(+:hits)
    for(int i = 0; i < num_samples; i++) {
        std::mt19937 gen(42 + i);
        std::uniform_real_distribution<float> dist(0.0f, box_size);
        float px = dist(gen);
        float py = dist(gen);
        float pz = dist(gen);

        bool hit = false;
        for(const auto& atom : atoms) {
            float dx = px - atom.x;
            float dy = py - atom.y;
            float dz = pz - atom.z;
            if(dx*dx + dy*dy + dz*dz < atom.r * atom.r) {
                hit = true;
                break;
            }
        }
        if(hit) {
            hits++;
        }
    }

    float total_volume = hits * vol_per_sample;
    std::cout << std::fixed << std::setprecision(6) << total_volume << std::endl;
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, "truth.cpp")
        exe_path = os.path.join(tmpdir, "truth_exe")
        with open(src_path, "w") as f:
            f.write(cpp_code)

        compile_cmd = ["g++", "-O3", "-fopenmp", src_path, "-o", exe_path]
        subprocess.run(compile_cmd, check=True, capture_output=True)

        run_cmd = [exe_path]
        result = subprocess.run(run_cmd, check=True, capture_output=True, text=True)
        return result.stdout.strip()

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did you save the output?"

    with open(result_path, "r") as f:
        student_result = f.read().strip()

    expected_result = get_expected_volume()

    assert student_result == expected_result, f"Result in {result_path} ({student_result}) does not match the deterministic expected volume ({expected_result})."

def test_executable_exists():
    exe_path = "/home/user/mc_volume"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did you compile the code?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_cpp_modifications():
    cpp_path = "/home/user/mc_volume.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    # The student should have removed the float reduction and used an integer counter or similar
    assert "reduction(+:total_volume)" not in content, "The code still uses floating-point reduction for total_volume, which is non-deterministic."