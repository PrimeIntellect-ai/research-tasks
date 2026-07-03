# test_final_state.py

import os
import json
import pytest

def test_analysis_out_notebook_exists_and_valid():
    notebook_path = "/home/user/analysis_out.ipynb"
    assert os.path.isfile(notebook_path), f"Output notebook {notebook_path} does not exist."

    with open(notebook_path, "r", encoding="utf-8") as f:
        try:
            nb_content = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{notebook_path} is not a valid JSON file.")

    assert "cells" in nb_content, f"{notebook_path} does not appear to be a valid Jupyter Notebook (missing 'cells')."

def test_mad_result_matches_expected():
    result_path = "/home/user/mad_result.txt"
    expected_path = "/home/user/data/expected_mad.txt"

    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."
    assert os.path.isfile(expected_path), f"Expected result file {expected_path} is missing."

    with open(result_path, "r", encoding="utf-8") as f:
        result_val = f.read().strip()

    with open(expected_path, "r", encoding="utf-8") as f:
        expected_val = f.read().strip()

    assert result_val == expected_val, f"MAD result '{result_val}' does not match expected '{expected_val}'."