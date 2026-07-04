# test_final_state.py
import os
import json
import csv
import math
import pytest

DIAGNOSTICS_DIR = "/home/user/diagnostics"

def test_extracted_metrics_csv_fixed():
    filepath = os.path.join(DIAGNOSTICS_DIR, "extracted_metrics.csv")
    assert os.path.isfile(filepath), f"File {filepath} is missing. Did the pipeline run successfully?"

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 4, f"Expected 4 rows in extracted_metrics.csv, got {len(rows)}"

    node_c = next((r for r in rows if r["Node"] == "NODE_C"), None)
    assert node_c is not None, "NODE_C is missing from extracted_metrics.csv"
    assert node_c["Latency"] == "0", f"NODE_C latency should be 0, got {node_c['Latency']}"

def test_health_scores_csv_fixed():
    filepath = os.path.join(DIAGNOSTICS_DIR, "health_scores.csv")
    assert os.path.isfile(filepath), f"File {filepath} is missing. Did the pipeline run successfully?"

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        scores = {row["Node"]: float(row["Score"]) for row in reader}

    expected_scores = {
        "NODE_A": ((100 - 50) * 0.4) + ((100 - 60) * 0.4) + ((1000 / (5 + 1.0)) * 0.2),
        "NODE_B": ((100 - 80) * 0.4) + ((100 - 90) * 0.4) + ((1000 / (20 + 1.0)) * 0.2),
        "NODE_C": ((100 - 20) * 0.4) + ((100 - 20) * 0.4) + ((1000 / (0 + 1.0)) * 0.2),
        "NODE_D": ((100 - 10) * 0.4) + ((100 - 15) * 0.4) + ((1000 / (2 + 1.0)) * 0.2),
    }

    for node, expected in expected_scores.items():
        assert node in scores, f"{node} missing from health_scores.csv"
        actual = scores[node]
        assert math.isclose(actual, expected, rel_tol=1e-3), \
            f"{node} score incorrect. Expected ~{expected:.4f}, got {actual}"

def test_final_report_json_fixed():
    filepath = os.path.join(DIAGNOSTICS_DIR, "final_report.json")
    assert os.path.isfile(filepath), f"File {filepath} is missing. Did the pipeline run successfully?"

    with open(filepath, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} is not valid JSON")

    expected_nodes = ["NODE_A", "NODE_B", "NODE_C", "NODE_D"]
    for node in expected_nodes:
        assert node in report, f"{node} is missing from final_report.json"

        val = report[node]
        assert isinstance(val, (int, float)), f"Value for {node} is not a number"
        assert not math.isnan(val), f"Value for {node} is NaN, normalization failed"
        assert not math.isinf(val), f"Value for {node} is Infinity, normalization failed"

        # Check convergence value. It should be approximately 126.39
        assert math.isclose(val, 126.39, abs_tol=1.0), \
            f"{node} value incorrect. Expected ~126.39, got {val}. Is the adjacency matrix row-normalized correctly?"

def test_venv_dependencies_installed():
    venv_dir = os.path.join(DIAGNOSTICS_DIR, "venv")
    assert os.path.isdir(venv_dir), "Virtual environment directory 'venv' is missing."

    # If the pipeline ran successfully and generated the final report, 
    # the python dependencies (numpy, networkx) must have been resolved.
    # We can verify the report exists as a strong proxy, but let's also check site-packages.
    site_packages = None
    for root, dirs, files in os.walk(os.path.join(venv_dir, "lib")):
        if "site-packages" in dirs:
            site_packages = os.path.join(root, "site-packages")
            break

    if site_packages:
        installed_packages = os.listdir(site_packages)
        has_numpy = any(p.startswith("numpy") for p in installed_packages)
        has_networkx = any(p.startswith("networkx") for p in installed_packages)
        assert has_numpy, "numpy is not installed in the virtual environment."
        assert has_networkx, "networkx is not installed in the virtual environment."