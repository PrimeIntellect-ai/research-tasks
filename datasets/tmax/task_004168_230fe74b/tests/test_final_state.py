# test_final_state.py
import os
import json
import re

def test_executed_notebook_exists_and_fixed():
    executed_nb_path = "/home/user/bfactor_workflow_executed.ipynb"
    assert os.path.exists(executed_nb_path), f"Executed notebook not found at {executed_nb_path}"

    with open(executed_nb_path, 'r') as f:
        try:
            nb_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{executed_nb_path} is not a valid JSON file."

    assert "cells" in nb_data, "Executed notebook does not contain 'cells'."

    # Check that the bug was fixed (bw_method='scott')
    found_scott = False
    found_ca_filter = False
    for cell in nb_data["cells"]:
        if cell.get("cell_type") == "code":
            source = "".join(cell.get("source", []))
            if "bw_method='scott'" in source.replace('"', "'"):
                found_scott = True
            if "atom_name == 'CA'" in source.replace('"', "'"):
                found_ca_filter = True

    assert found_scott, "The KDE bandwidth method was not changed to 'scott' in the notebook."
    assert found_ca_filter, "The filtering for 'CA' atoms was lost or altered."

def test_results_file_and_value():
    results_path = "/home/user/results.txt"
    assert os.path.exists(results_path), f"Results file not found at {results_path}"

    with open(results_path, 'r') as f:
        content = f.read().strip()

    # Expecting format "Integral: <float>"
    match = re.search(r"Integral:\s*([0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)", content)
    assert match is not None, f"Results file does not contain a valid 'Integral: <value>' string. Content: {content}"

    integral_val = float(match.group(1))

    # The true integral for the synthetic data should be around 0.99
    # We check if it's in a reasonable range (e.g., 0.9 to 1.0) indicating successful integration
    assert 0.9 < integral_val <= 1.0, f"Calculated integral {integral_val} is out of expected bounds (0.9, 1.0]. The KDE fix might not be applied correctly."