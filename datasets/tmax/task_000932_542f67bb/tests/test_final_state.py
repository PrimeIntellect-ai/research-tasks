# test_final_state.py

import os
import json
import pytest

def test_notebooks_exist():
    """Verify that the input and output Jupyter notebooks exist."""
    input_nb = "/home/user/analysis.ipynb"
    output_nb = "/home/user/analysis_out.ipynb"

    assert os.path.exists(input_nb), f"Expected notebook {input_nb} is missing."
    assert os.path.isfile(input_nb), f"{input_nb} is not a file."

    assert os.path.exists(output_nb), f"Expected executed notebook {output_nb} is missing."
    assert os.path.isfile(output_nb), f"{output_nb} is not a file."

def test_results_json():
    """Verify that results.json exists and contains the correct values."""
    results_file = "/home/user/results.json"

    assert os.path.exists(results_file), f"Expected results file {results_file} is missing."
    assert os.path.isfile(results_file), f"{results_file} is not a file."

    with open(results_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not valid JSON.")

    assert "final_V" in data, "Key 'final_V' is missing from results.json."
    assert "best_primer" in data, "Key 'best_primer' is missing from results.json."

    # Check final_V
    expected_v = 800.0
    assert isinstance(data["final_V"], float), f"'final_V' must be a float, got {type(data['final_V']).__name__}."
    assert data["final_V"] == expected_v, f"Expected 'final_V' to be {expected_v}, got {data['final_V']}."

    # Check best_primer
    expected_primer = "GCGGCCGC"
    assert data["best_primer"] == expected_primer, f"Expected 'best_primer' to be '{expected_primer}', got '{data['best_primer']}'."