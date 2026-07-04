# test_final_state.py

import os
import subprocess
import pytest

def test_preprocess_c_exists():
    file_path = "/home/user/preprocess.c"
    assert os.path.exists(file_path), f"The C program {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} should be a file."

def test_tune_sh_exists():
    file_path = "/home/user/tune.sh"
    assert os.path.exists(file_path), f"The bash script {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} should be a file."

def test_best_t_txt_content():
    file_path = "/home/user/best_t.txt"
    assert os.path.exists(file_path), f"The output file {file_path} is missing. Did the bash script run?"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "150", f"Expected /home/user/best_t.txt to contain '150', but found '{content}'."

def test_preprocess_c_logic():
    # Compile the C program to a temporary executable
    c_file = "/home/user/preprocess.c"
    exe_file = "/tmp/preprocess_test_exe"
    data_file = "/home/user/raw_data.csv"

    compile_proc = subprocess.run(["gcc", c_file, "-o", exe_file], capture_output=True)
    assert compile_proc.returncode == 0, f"Failed to compile {c_file}:\n{compile_proc.stderr.decode()}"

    # Run with T=100, expected mean is 45.5
    run_proc = subprocess.run([exe_file, data_file, "100"], capture_output=True, text=True)
    assert run_proc.returncode == 0, f"Running the compiled C program failed:\n{run_proc.stderr}"

    output = run_proc.stdout.strip()
    try:
        mean_val = float(output)
    except ValueError:
        pytest.fail(f"Expected the C program to output a numeric mean, but got: '{output}'")

    assert abs(mean_val - 45.5) < 0.01, f"Expected mean for T=100 to be 45.5, but got {mean_val}"

    # Run with T=150, expected mean is 58.0
    run_proc2 = subprocess.run([exe_file, data_file, "150"], capture_output=True, text=True)
    assert run_proc2.returncode == 0, f"Running the compiled C program failed:\n{run_proc2.stderr}"

    output2 = run_proc2.stdout.strip()
    try:
        mean_val2 = float(output2)
    except ValueError:
        pytest.fail(f"Expected the C program to output a numeric mean, but got: '{output2}'")

    assert abs(mean_val2 - 58.0) < 0.01, f"Expected mean for T=150 to be 58.0, but got {mean_val2}"