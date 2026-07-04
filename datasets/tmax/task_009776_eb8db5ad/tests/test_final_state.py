# test_final_state.py

import os
import json
import math
import pytest

def test_primers_fasta_exists_and_valid():
    fasta_path = "/home/user/primers.fasta"
    assert os.path.isfile(fasta_path), f"File {fasta_path} does not exist. Did you run the sequence generator?"

    with open(fasta_path, "r") as f:
        lines = f.readlines()

    # 10,000 sequences, each taking 2 lines (header + sequence)
    assert len(lines) == 20000, f"Expected 20000 lines in {fasta_path}, but found {len(lines)}."
    assert lines[0].startswith(">primer_0"), "First sequence header is incorrect."

def test_cpu_prof_exists():
    prof_path = "/home/user/cpu.prof"
    assert os.path.isfile(prof_path), f"File {prof_path} does not exist. Did you add pprof profiling and run the Go app?"
    assert os.path.getsize(prof_path) > 0, f"File {prof_path} is empty."

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert "integral_value" in report, "Key 'integral_value' missing from report.json."
    assert "bottleneck_function" in report, "Key 'bottleneck_function' missing from report.json."

    integral_value = report["integral_value"]
    assert isinstance(integral_value, (int, float)), "integral_value must be a number."
    assert math.isclose(integral_value, 1.0, abs_tol=0.001), f"integral_value is {integral_value}, expected ~1.0000."

    bottleneck_function = report["bottleneck_function"]
    assert bottleneck_function == "main.slowAlignmentScoring", f"bottleneck_function is '{bottleneck_function}', expected 'main.slowAlignmentScoring'."