# test_final_state.py
import os
import json

def test_compiled_executable_exists():
    path = "/home/user/generate_pdb"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_simulated_pdb_exists():
    path = "/home/user/simulated.pdb"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        content = f.read()
    assert "ATOM" in content, "simulated.pdb does not seem to contain ATOM records."

def test_analysis_results_json():
    path = "/home/user/analysis_results.json"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    try:
        with open(path, "r") as f:
            results = json.load(f)
    except json.JSONDecodeError:
        assert False, f"File {path} is not valid JSON."

    assert "best_fit" in results, "Key 'best_fit' missing in analysis_results.json"
    assert "aic_normal" in results, "Key 'aic_normal' missing in analysis_results.json"
    assert "aic_gamma" in results, "Key 'aic_gamma' missing in analysis_results.json"

    assert results["best_fit"] == "Gamma", f"Expected 'best_fit' to be 'Gamma', got {results['best_fit']}"

    assert isinstance(results["aic_normal"], (int, float)), "aic_normal must be a number"
    assert isinstance(results["aic_gamma"], (int, float)), "aic_gamma must be a number"

    assert results["aic_gamma"] < results["aic_normal"], "Expected aic_gamma to be less than aic_normal"