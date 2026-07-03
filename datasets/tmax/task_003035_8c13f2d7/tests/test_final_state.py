# test_final_state.py
import os
import json
import math
import subprocess

def test_run_eval_script_exists_and_executable():
    script_path = "/home/user/run_eval.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_metrics_json_format_and_values():
    json_path = "/home/user/metrics.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert "mean_accuracy" in metrics, "Missing 'mean_accuracy' in metrics.json"
    assert "margin_of_error" in metrics, "Missing 'margin_of_error' in metrics.json"
    assert "hypothesis_passed" in metrics, "Missing 'hypothesis_passed' in metrics.json"

    # Calculate the expected values
    accuracies = []
    py_script = "/home/user/train_and_plot.py"

    # We run the script with MPLBACKEND=Agg to ensure it doesn't crash here 
    # if the student only exported it in their bash script.
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"

    for seed in range(1, 31):
        result = subprocess.run(
            ["python3", py_script, str(seed)],
            env=env,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Python script failed for seed {seed}."
        try:
            acc = float(result.stdout.strip())
            accuracies.append(acc)
        except ValueError:
            assert False, f"Could not parse accuracy from output: {result.stdout}"

    n = len(accuracies)
    mean_acc = sum(accuracies) / n
    variance = sum((x - mean_acc) ** 2 for x in accuracies) / (n - 1)
    std_dev = math.sqrt(variance)
    margin = 1.96 * (std_dev / math.sqrt(n))
    hypothesis = (mean_acc - margin) > 0.80

    expected_mean = round(mean_acc, 4)
    expected_margin = round(margin, 4)

    assert math.isclose(metrics["mean_accuracy"], expected_mean, abs_tol=1e-4), \
        f"Expected mean_accuracy {expected_mean}, got {metrics['mean_accuracy']}"

    assert math.isclose(metrics["margin_of_error"], expected_margin, abs_tol=1e-4), \
        f"Expected margin_of_error {expected_margin}, got {metrics['margin_of_error']}"

    assert metrics["hypothesis_passed"] == hypothesis, \
        f"Expected hypothesis_passed {hypothesis}, got {metrics['hypothesis_passed']}"

def test_plot_generated():
    # The script should have generated plot.png either in the current directory or /home/user/
    # The task runs it from /home/user/run_eval.sh
    plot_path = "plot.png"
    if not os.path.exists(plot_path):
        plot_path = "/home/user/plot.png"
    assert os.path.isfile(plot_path), "plot.png was not generated. The plotting code might have been removed or failed."