# test_final_state.py

import os
import pytest

def test_libextractor_compiled():
    path = "/home/user/libextractor.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist. Did you compile extractor.c?"

def test_pipeline_test_script_exists():
    path = "/home/user/pipeline_test.py"
    assert os.path.isfile(path), f"Python script {path} does not exist."

def test_pipeline_result_log():
    path = "/home/user/pipeline_result.log"
    assert os.path.isfile(path), f"Result log {path} does not exist. Did the pipeline script run successfully?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "SUCCESS_201_METADATA_OK"
    assert content == expected, f"Expected '{expected}' in {path}, but found '{content}'."