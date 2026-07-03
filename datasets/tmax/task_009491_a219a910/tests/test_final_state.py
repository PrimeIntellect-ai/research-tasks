# test_final_state.py
import os
import json
import subprocess

def test_scripts_exist():
    scripts = [
        "/home/user/mc_generator.py",
        "/home/user/evaluator.py",
        "/home/user/test_convergence.sh"
    ]
    for script in scripts:
        assert os.path.exists(script), f"Script {script} does not exist"

def test_convergence_script_execution():
    script_path = "/home/user/test_convergence.sh"

    # Run the bash script
    result = subprocess.run(["bash", script_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"test_convergence.sh failed with error: {result.stderr}"

    results_file = "/home/user/results.json"
    assert os.path.exists(results_file), "results.json was not created"

    with open(results_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not valid JSON"

    assert "100" in data and "1000" in data and "10000" in data, "results.json missing required keys"

    v100 = float(data["100"])
    v1000 = float(data["1000"])
    v10000 = float(data["10000"])

    # Check convergence (approximate)
    # The distance for 10000 should generally be less than for 100
    assert v10000 < v100, f"Convergence not observed: dist(10000)={v10000} >= dist(100)={v100}"

def test_mc_generator_distribution():
    script_path = "/home/user/mc_generator.py"
    output_csv = "/home/user/test_10000.csv"

    if os.path.exists(output_csv):
        os.remove(output_csv)

    # Run the generator
    result = subprocess.run(["python3", script_path, "10000", "42", output_csv], capture_output=True, text=True)
    assert result.returncode == 0, f"mc_generator.py failed: {result.stderr}"

    assert os.path.exists(output_csv), "Output CSV not created by mc_generator.py"

    # Calculate mean of x^2 + y^2 + z^2
    sum_r2 = 0.0
    count = 0
    with open(output_csv, "r") as f:
        header = f.readline().strip()
        assert header == "x,y,z", "Incorrect CSV header"
        for line in f:
            if not line.strip(): 
                continue
            parts = line.strip().split(",")
            assert len(parts) == 3, f"Invalid row format: {line}"
            x, y, z = map(float, parts)
            sum_r2 += x*x + y*y + z*z
            count += 1

    assert count == 10000, f"Expected 10000 rows, got {count}"

    mean_r2 = sum_r2 / count
    # Expected value is 1.8. Allow some tolerance
    assert 1.7 < mean_r2 < 1.9, f"Mean r^2 is {mean_r2}, expected ~1.8"