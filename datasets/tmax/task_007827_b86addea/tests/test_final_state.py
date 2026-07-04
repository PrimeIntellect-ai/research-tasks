# test_final_state.py
import os
import json
import subprocess
import pytest

def test_results_json_exists():
    assert os.path.isfile("/home/user/evaluation_pipeline/results.json"), "The results.json file was not generated in /home/user/evaluation_pipeline/."

def test_results_json_contents():
    results_path = "/home/user/evaluation_pipeline/results.json"
    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    assert "alpha" in data, "Key 'alpha' is missing from results.json."
    assert "beta" in data, "Key 'beta' is missing from results.json."
    assert "best_model" in data, "Key 'best_model' is missing from results.json."

    alpha = data["alpha"]
    beta = data["beta"]

    # Alpha expectations
    assert abs(alpha.get("fold_1_mse", -1) - 0.25) < 1e-4, f"Alpha fold_1_mse is incorrect. Got {alpha.get('fold_1_mse')}"
    assert abs(alpha.get("fold_2_mse", -1) - 0.25) < 1e-4, f"Alpha fold_2_mse is incorrect. Got {alpha.get('fold_2_mse')}"
    assert abs(alpha.get("fold_3_mse", -1) - 0.625) < 1e-4, f"Alpha fold_3_mse is incorrect. Got {alpha.get('fold_3_mse')}"
    assert abs(alpha.get("fold_4_mse", -1) - 1.0) < 1e-4, f"Alpha fold_4_mse is incorrect. Got {alpha.get('fold_4_mse')}"
    assert abs(alpha.get("fold_5_mse", -1) - 0.25) < 1e-4, f"Alpha fold_5_mse is incorrect. Got {alpha.get('fold_5_mse')}"
    assert abs(alpha.get("average_mse", -1) - 0.475) < 1e-4, f"Alpha average_mse is incorrect. Got {alpha.get('average_mse')}"

    # Beta expectations
    assert abs(beta.get("fold_1_mse", -1) - 3.125) < 1e-4, f"Beta fold_1_mse is incorrect. Got {beta.get('fold_1_mse')}"
    assert abs(beta.get("fold_2_mse", -1) - 1.625) < 1e-4, f"Beta fold_2_mse is incorrect. Got {beta.get('fold_2_mse')}"
    assert abs(beta.get("fold_3_mse", -1) - 5.125) < 1e-4, f"Beta fold_3_mse is incorrect. Got {beta.get('fold_3_mse')}"
    assert abs(beta.get("fold_4_mse", -1) - 25.0) < 1e-4, f"Beta fold_4_mse is incorrect. Got {beta.get('fold_4_mse')}"
    assert abs(beta.get("fold_5_mse", -1) - 5.125) < 1e-4, f"Beta fold_5_mse is incorrect. Got {beta.get('fold_5_mse')}"
    assert abs(beta.get("average_mse", -1) - 8.0) < 1e-4, f"Beta average_mse is incorrect. Got {beta.get('average_mse')}"

    assert data["best_model"] == "alpha", f"Expected best_model to be 'alpha', got '{data['best_model']}'"

def test_go_files_exist():
    assert os.path.isfile("/home/user/evaluation_pipeline/main.go"), "main.go is missing from /home/user/evaluation_pipeline/."
    assert os.path.isfile("/home/user/evaluation_pipeline/math_test.go"), "math_test.go is missing from /home/user/evaluation_pipeline/."

def test_go_tests_pass():
    pipeline_dir = "/home/user/evaluation_pipeline"
    result = subprocess.run(
        ["go", "test"],
        cwd=pipeline_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'go test' failed in {pipeline_dir}.\nStdout: {result.stdout}\nStderr: {result.stderr}"