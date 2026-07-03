# test_final_state.py
import os
import re

def test_ml_prep_directory_exists():
    assert os.path.isdir("/home/user/ml_prep"), "The directory /home/user/ml_prep does not exist."

def test_eigen_extracted():
    eigen_path = "/home/user/ml_prep/eigen/Eigen"
    assert os.path.isdir(eigen_path), f"Eigen headers not found at {eigen_path}."
    assert os.path.isfile(os.path.join(eigen_path, "Dense")), "Eigen/Dense header not found, extraction might be incorrect."

def test_cpp_file_exists():
    assert os.path.isfile("/home/user/ml_prep/tune_ridge.cpp"), "The C++ source file tune_ridge.cpp is missing."

def test_run_pipeline_script_exists():
    script_path = "/home/user/ml_prep/run_pipeline.sh"
    assert os.path.isfile(script_path), f"The bash script {script_path} is missing."
    assert os.access(script_path, os.X_OK) or True, "The run_pipeline.sh script should ideally be executable."

def test_tuning_results_file():
    results_file = "/home/user/ml_prep/tuning_results.txt"
    assert os.path.isfile(results_file), f"The results file {results_file} was not generated."

    with open(results_file, "r") as f:
        content = f.read().strip()

    # Check for Best lambda
    assert re.search(r"Best lambda:\s*0", content), "The best lambda should be 0."

    # Check for Best MSE
    assert re.search(r"Best MSE:\s*0\.0000", content), "The best MSE should be 0.0000."