# test_final_state.py
import os
import re

def test_report_exists_and_content_is_correct():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"File {report_path} is missing. Did the program run and generate the report?"

    with open(report_path, 'r') as f:
        content = f.read()

    assert "Model: BetaNet" in content, "The report does not contain 'Model: BetaNet'."
    assert "Valid Samples: 7" in content, "The report does not contain 'Valid Samples: 7'. Make sure data filtering is correct."

    # Extract Mean of Means
    mean_match = re.search(r"Mean of Means:\s*([0-9.]+)", content)
    assert mean_match is not None, "Could not find 'Mean of Means' in the report."
    mean_val = float(mean_match.group(1))
    assert abs(mean_val - 0.8542) <= 0.0002, f"Expected Mean of Means around 0.8542, but got {mean_val}."

    # Extract CI bounds
    ci_match = re.search(r"95% CI:\s*\[([0-9.]+),\s*([0-9.]+)\]", content)
    assert ci_match is not None, "Could not find '95% CI' bounds in the report."
    lower_bound = float(ci_match.group(1))
    upper_bound = float(ci_match.group(2))

    assert abs(lower_bound - 0.8343) <= 0.0002, f"Expected lower bound around 0.8343, but got {lower_bound}."
    assert abs(upper_bound - 0.8743) <= 0.0002, f"Expected upper bound around 0.8743, but got {upper_bound}."

def test_cpp_source_and_binary_exist():
    cpp_path = "/home/user/mlops_etl.cpp"
    bin_path = "/home/user/mlops_etl"

    assert os.path.isfile(cpp_path), f"C++ source code {cpp_path} is missing."
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."