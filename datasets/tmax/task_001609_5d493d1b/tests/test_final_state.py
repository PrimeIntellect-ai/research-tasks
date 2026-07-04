# test_final_state.py

import os
import json
import pytest

def test_graph_tool_installed_and_fixed():
    """Check if the graph_tool was installed and the python2 misconfiguration was fixed."""
    path = "/usr/local/bin/graph_tool"
    assert os.path.isfile(path), f"Executable {path} was not installed. Did you run 'make install'?"

    with open(path, "r") as f:
        content = f.read()

    assert "PYTHON_EXE=python3" in content, "The graph_tool executable wrapper was not fixed to use 'python3'."
    assert "PYTHON_EXE=python2" not in content, "The graph_tool executable wrapper still uses 'python2'."

def test_analyze_script_exists():
    """Check if the analyze.sh script was created."""
    path = "/home/user/analyze.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."

def test_results_json_metric():
    """Check if results.json exists, is valid, and the metric threshold is met."""
    path = "/home/user/results.json"
    assert os.path.isfile(path), f"Results file {path} does not exist. Did the script run successfully?"

    with open(path, "r") as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "ci_lower" in res, "Missing 'ci_lower' key in results.json."
    assert "ci_upper" in res, "Missing 'ci_upper' key in results.json."

    # Reference acceptable bounds for a typical 500-iteration bootstrap
    REF_LOWER = 45.1
    REF_UPPER = 52.8

    err_lower = abs(res['ci_lower'] - REF_LOWER) / REF_LOWER
    err_upper = abs(res['ci_upper'] - REF_UPPER) / REF_UPPER
    max_err = max(err_lower, err_upper)

    assert max_err <= 0.05, (
        f"Confidence intervals are not within the 5% tolerance. "
        f"Max error: {max_err:.4f} (Threshold: <= 0.05). "
        f"Got ci_lower={res['ci_lower']}, ci_upper={res['ci_upper']}."
    )