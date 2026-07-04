# test_final_state.py
import os
import csv
import stat
import pytest

def test_integrator_fixed():
    integrator_path = "/home/user/simulation/integrator.go"
    assert os.path.isfile(integrator_path), f"{integrator_path} is missing."

    with open(integrator_path, "r") as f:
        content = f.read()

    assert "tol / err" in content or "tol/err" in content, "The step size adaptation logic was not correctly inverted to (tol / err)."
    assert "0.1" in content, "Clamping upper bound (0.1) not found in integrator.go."
    assert "1e-6" in content, "Clamping lower bound (1e-6) not found in integrator.go."

def test_pipeline_script():
    script_path = "/home/user/simulation/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_cpu_profile_generated():
    prof_path = "/home/user/simulation/cpu.prof"
    assert os.path.isfile(prof_path), f"{prof_path} was not generated. Ensure run_pipeline.sh runs the app with profiling enabled."
    assert os.path.getsize(prof_path) > 0, f"{prof_path} is empty."

def test_output_csv_format():
    out_path = "/home/user/simulation/output.csv"
    assert os.path.isfile(out_path), f"{out_path} does not exist."

    with open(out_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{out_path} is empty."

    for i, row in enumerate(rows):
        assert len(row) == 2, f"Expected exactly 2 columns in {out_path} (time, state), but row {i+1} has {len(row)} columns."
        try:
            float(row[0])
            float(row[1])
        except ValueError:
            pytest.fail(f"Non-float values found in {out_path} at row {i+1}: {row}")

def test_metric_log():
    metric_path = "/home/user/simulation/metric.log"
    assert os.path.isfile(metric_path), f"{metric_path} does not exist."

    with open(metric_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"{metric_path} does not contain a valid float. Found: '{content}'")

    assert val < 0.1, f"Metric value {val} is suspiciously high (>= 0.1). The 1-Wasserstein distance approximation should be small if the simulation is correct."