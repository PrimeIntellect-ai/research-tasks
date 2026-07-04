# test_final_state.py
import os
import subprocess
import pytest

def setup_reference_cleaner():
    cpp_code = """
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <functional>

using namespace std;

bool is_valid_numeric(const string& s) {
    if (s.empty()) return false;
    size_t start = 0;
    if (s[0] == '-') start = 1;
    if (start == s.length()) return false;
    bool has_dot = false;
    bool has_digit = false;
    for (size_t i = start; i < s.length(); ++i) {
        if (s[i] == '.') {
            if (has_dot) return false;
            has_dot = true;
        } else if (isdigit(s[i])) {
            has_digit = true;
        } else {
            return false;
        }
    }
    return has_digit;
}

int main(int argc, char** argv) {
    if (argc != 3) return 1;
    ifstream in(argv[1]);
    ofstream out(argv[2]);
    string line;
    string salt = "z9X_#Lq2";

    while (getline(in, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        string ts, temp, volt, rpm;

        if (!getline(ss, ts, ',')) continue;
        if (!getline(ss, temp, ',')) continue;
        if (!getline(ss, volt, ',')) continue;
        if (!getline(ss, rpm, ',')) continue;

        // Remove potential trailing carriage returns
        if (!rpm.empty() && rpm.back() == '\\r') rpm.pop_back();

        if (!is_valid_numeric(temp) || !is_valid_numeric(volt) || !is_valid_numeric(rpm)) {
            continue;
        }

        auto write_row = [&](const string& sensor, const string& val) {
            string key = ts + "_" + sensor + "_" + val + "_" + salt;
            out << ts << "," << sensor << "," << val << "," << std::hash<std::string>{}(key) << "\\n";
        };

        write_row("temp", temp);
        write_row("volt", volt);
        write_row("rpm", rpm);
    }
    return 0;
}
"""
    ref_bin = "/tmp/ref_cleaner"
    if not os.path.exists(ref_bin):
        cpp_path = "/tmp/ref_cleaner.cpp"
        with open(cpp_path, "w") as f:
            f.write(cpp_code)
        subprocess.run(["g++", "-O3", "-std=c++17", cpp_path, "-o", ref_bin], check=True)
    return ref_bin

def test_cleaner_binary_exists():
    binary_path = "/home/user/cleaner"
    assert os.path.isfile(binary_path), f"Cleaner binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Cleaner binary at {binary_path} is not executable"

def test_process_all_script_exists():
    script_path = "/home/user/process_all.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_clean_corpus_preserved():
    ref_bin = setup_reference_cleaner()
    clean_dir = "/app/corpus/clean"
    student_bin = "/home/user/cleaner"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    failed_files = []
    total_files = 0

    for fname in os.listdir(clean_dir):
        if not fname.endswith(".csv"): continue
        total_files += 1
        in_path = os.path.join(clean_dir, fname)
        ref_out = f"/tmp/ref_clean_{fname}"
        stu_out = f"/tmp/stu_clean_{fname}"

        subprocess.run([ref_bin, in_path, ref_out], check=True)
        result = subprocess.run([student_bin, in_path, stu_out], capture_output=True)

        if result.returncode != 0 or not os.path.exists(stu_out):
            failed_files.append(fname)
            continue

        with open(ref_out, "r") as f1, open(stu_out, "r") as f2:
            if f1.read().strip() != f2.read().strip():
                failed_files.append(fname)

    assert not failed_files, f"{len(failed_files)} of {total_files} clean files modified incorrectly: {failed_files}"

def test_evil_corpus_rejected():
    ref_bin = setup_reference_cleaner()
    evil_dir = "/app/corpus/evil"
    student_bin = "/home/user/cleaner"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    failed_files = []
    total_files = 0

    for fname in os.listdir(evil_dir):
        if not fname.endswith(".csv"): continue
        total_files += 1
        in_path = os.path.join(evil_dir, fname)
        ref_out = f"/tmp/ref_evil_{fname}"
        stu_out = f"/tmp/stu_evil_{fname}"

        subprocess.run([ref_bin, in_path, ref_out], check=True)
        result = subprocess.run([student_bin, in_path, stu_out], capture_output=True)

        if result.returncode != 0 or not os.path.exists(stu_out):
            failed_files.append(fname)
            continue

        with open(ref_out, "r") as f1, open(stu_out, "r") as f2:
            if f1.read().strip() != f2.read().strip():
                failed_files.append(fname)

    assert not failed_files, f"{len(failed_files)} of {total_files} evil files bypassed validation: {failed_files}"