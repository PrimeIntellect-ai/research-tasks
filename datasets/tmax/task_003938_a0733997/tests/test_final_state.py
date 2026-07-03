# test_final_state.py
import os
import pytest

def test_pipeline_success_out_exists():
    assert os.path.isfile('/home/user/pipeline_success.out'), "/home/user/pipeline_success.out does not exist. Did you run the pipeline and save the output?"

def test_pipeline_success_out_content():
    with open('/home/user/pipeline_success.out', 'r') as f:
        content = f.read()

    assert "File: /home/user/logs/batch_3.csv | Mean:" in content, "The output for batch_3.csv is missing or incorrectly formatted. The pipeline might have crashed or the output format was altered."

    lines = [line.strip() for line in content.split('\n') if line.strip()]
    assert len(lines) == 4, f"Expected exactly 4 lines of output in /home/user/pipeline_success.out, but found {len(lines)}."

def test_no_errors_in_output():
    with open('/home/user/pipeline_success.out', 'r') as f:
        content = f.read()
    assert "Domain error" not in content, "The output still contains a 'Domain error'. The numerical instability was not fixed."
    assert "std::runtime_error" not in content, "The output contains a runtime error. The pipeline did not complete successfully."

def test_cpp_source_modified():
    with open('/home/user/src/sensor_aggregator.cpp', 'r') as f:
        content = f.read()

    # The original vulnerable line
    vulnerable_line = "float variance = (sum_sq / values.size()) - (mean * mean);"
    assert vulnerable_line not in content, "The C++ source code still uses the naive variance formula. You need to implement a numerically stable method."