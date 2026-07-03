# test_final_state.py
import os
import json
import pytest

def test_metrics_json_exists_and_format():
    metrics_path = "/home/user/metrics.json"
    assert os.path.isfile(metrics_path), f"Missing metrics file: {metrics_path}"

    with open(metrics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} is not valid JSON.")

    assert "ci_lower" in data, "metrics.json missing 'ci_lower'"
    assert "ci_upper" in data, "metrics.json missing 'ci_upper'"

    try:
        agent_lower = float(data["ci_lower"])
        agent_upper = float(data["ci_upper"])
    except ValueError:
        pytest.fail("ci_lower and ci_upper must be numeric.")

    assert -1.0 <= agent_lower <= 1.0, f"ci_lower {agent_lower} is out of valid Pearson correlation bounds [-1, 1]"
    assert -1.0 <= agent_upper <= 1.0, f"ci_upper {agent_upper} is out of valid Pearson correlation bounds [-1, 1]"
    assert agent_lower < agent_upper, f"ci_lower ({agent_lower}) must be less than ci_upper ({agent_upper})"

def test_cpp_code_exists():
    cpp_path = "/home/user/analysis.cpp"
    assert os.path.isfile(cpp_path), f"Missing C++ analysis file: {cpp_path}"

    with open(cpp_path, 'r') as f:
        content = f.read()

    assert "mt19937" in content or "std::mt19937" in content, "C++ code does not seem to use mt19937 for random number generation."
    assert "42" in content, "C++ code does not seem to use the seed 42."
    assert "10000" in content or "10,000" in content or "10000.0" in content, "C++ code does not seem to use B=10000 bootstrap iterations."