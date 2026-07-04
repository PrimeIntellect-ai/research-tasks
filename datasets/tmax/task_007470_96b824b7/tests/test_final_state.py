# test_final_state.py

import os
import re

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_pipeline_script_content():
    script_path = "/home/user/run_pipeline.sh"
    with open(script_path, "r") as f:
        content = f.read()

    # Check shebang
    assert content.startswith("#!/bin/bash") or content.startswith("#!/usr/bin/env bash"), \
        "Script does not have a proper bash shebang."

    # Check exports
    assert re.search(r"export\s+OPENBLAS_NUM_THREADS=2\b", content), \
        "Script does not correctly export OPENBLAS_NUM_THREADS=2."
    assert re.search(r"export\s+OMP_NUM_THREADS=2\b", content), \
        "Script does not correctly export OMP_NUM_THREADS=2."

def test_predictions_output():
    predictions_path = "/home/user/predictions.txt"
    assert os.path.isfile(predictions_path), f"Output file {predictions_path} does not exist. Did you run the script?"

    with open(predictions_path, "r") as f:
        content = f.read().strip()

    expected_content = "Inference results for feature_A: [2.0, 4.0, 6.0, 8.0, 10.0]"
    assert content == expected_content, \
        f"Content of {predictions_path} is incorrect. Expected: '{expected_content}', Got: '{content}'"