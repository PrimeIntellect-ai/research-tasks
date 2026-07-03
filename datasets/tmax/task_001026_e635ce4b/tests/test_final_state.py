# test_final_state.py

import os
import re

def test_model_output_exists_and_correct():
    output_path = "/home/user/model_output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    # The expected output values
    expected_intercept = "2.1462"
    expected_sensor = "0.2248"
    expected_temp = "-0.0968"

    assert f"Intercept: {expected_intercept}" in content, "Intercept value is missing or incorrect."
    assert f"Coefficient sensor_count: {expected_sensor}" in content, "Coefficient sensor_count is missing or incorrect."
    assert f"Coefficient temperature_celsius: {expected_temp}" in content, "Coefficient temperature_celsius is missing or incorrect."

def test_train_c_exists():
    c_file_path = "/home/user/train.c"
    assert os.path.isfile(c_file_path), f"C source file {c_file_path} does not exist."

def test_gsl_installed():
    # Check if gsl library is present in standard locations
    assert os.path.exists("/usr/include/gsl/gsl_fit.h") or os.path.exists("/usr/include/gsl/gsl_multifit.h"), "GSL library headers not found. Was libgsl-dev installed?"