# test_final_state.py

import os
import json
import math

def test_report_json_exists_and_correct():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Missing file: {report_path}. The report was not generated."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {report_path} is not a valid JSON."

    required_keys = {
        "t_stat",
        "p_value",
        "exp_A_success_alpha",
        "exp_A_success_beta"
    }

    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in report.json: {missing_keys}"

    # Ground truth values derived from the task definition
    expected_t_stat = 1.3406
    expected_p_value = 0.2312
    expected_alpha = 4
    expected_beta = 3

    assert math.isclose(data["t_stat"], expected_t_stat, abs_tol=1e-3), \
        f"Expected t_stat around {expected_t_stat}, got {data['t_stat']}"

    assert math.isclose(data["p_value"], expected_p_value, abs_tol=1e-3), \
        f"Expected p_value around {expected_p_value}, got {data['p_value']}"

    assert data["exp_A_success_alpha"] == expected_alpha, \
        f"Expected exp_A_success_alpha to be {expected_alpha}, got {data['exp_A_success_alpha']}"

    assert data["exp_A_success_beta"] == expected_beta, \
        f"Expected exp_A_success_beta to be {expected_beta}, got {data['exp_A_success_beta']}"