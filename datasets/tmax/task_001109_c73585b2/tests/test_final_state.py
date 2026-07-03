# test_final_state.py
import os
import json

def test_final_temperatures_json():
    json_path = "/home/user/final_temperatures.json"
    assert os.path.isfile(json_path), f"Expected file {json_path} does not exist. Did you export the temperatures?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not valid JSON."

    assert len(data) == 7, f"Expected exactly 7 nodes after refinement, but found {len(data)} in {json_path}."

    assert "0" in data, "Node '0' missing from final temperatures."
    assert "1" in data, "Node '1' missing from final temperatures."

    t0 = float(data["0"])
    t1 = float(data["1"])

    assert t0 < 100.0, f"Node 0 did not cool down as expected. Final temp: {t0}"
    assert t1 > 0.0, f"Node 1 did not warm up as expected. Final temp: {t1}"

def test_thermal_plot_exists():
    plot_path = "/home/user/thermal_plot.png"
    assert os.path.isfile(plot_path), f"Expected plot {plot_path} does not exist. Did you save the plot?"
    assert os.path.getsize(plot_path) > 0, f"Plot {plot_path} is empty."

def test_bug_fixed_in_simulate():
    simulate_path = "/home/user/simulate.py"
    assert os.path.isfile(simulate_path), f"File {simulate_path} does not exist."

    with open(simulate_path, "r") as f:
        content = f.read()

    assert "dt = dt * 2.0" not in content, "The bug 'dt = dt * 2.0' is still present in simulate.py. It should be changed to reduce the step size."