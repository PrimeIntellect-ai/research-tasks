# test_final_state.py
import os
import math

def test_fixed_scripts_and_outputs_exist():
    """Check that the required files have been created."""
    experiment_dir = "/home/user/experiment"

    fixed_train = os.path.join(experiment_dir, "fixed_train.py")
    assert os.path.isfile(fixed_train), f"Missing {fixed_train}"

    fixed_preds = os.path.join(experiment_dir, "fixed_predictions.csv")
    assert os.path.isfile(fixed_preds), f"Missing {fixed_preds}"

    compare_sh = os.path.join(experiment_dir, "compare.sh")
    assert os.path.isfile(compare_sh), f"Missing {compare_sh}"

    metrics_txt = os.path.join(experiment_dir, "metrics.txt")
    assert os.path.isfile(metrics_txt), f"Missing {metrics_txt}"

def test_predictions_and_metrics_correctness():
    """Calculate the expected MAE and verify metrics.txt."""
    experiment_dir = "/home/user/experiment"

    data_file = os.path.join(experiment_dir, "data.csv")
    leaky_preds_file = os.path.join(experiment_dir, "leaky_predictions.csv")
    fixed_preds_file = os.path.join(experiment_dir, "fixed_predictions.csv")
    metrics_txt = os.path.join(experiment_dir, "metrics.txt")

    # Read test targets (last 20 rows)
    with open(data_file, "r") as f:
        lines = f.read().strip().split("\n")

    header = lines[0]
    data_lines = lines[1:]
    assert len(data_lines) == 100, "data.csv should have exactly 100 data rows"

    test_targets = [float(line.split(",")[2]) for line in data_lines[-20:]]

    # Read leaky predictions
    with open(leaky_preds_file, "r") as f:
        leaky_preds = [float(x) for x in f.read().strip().split("\n")]
    assert len(leaky_preds) == 20, "leaky_predictions.csv should have exactly 20 rows"

    # Read fixed predictions
    with open(fixed_preds_file, "r") as f:
        fixed_preds = [float(x) for x in f.read().strip().split("\n")]
    assert len(fixed_preds) == 20, "fixed_predictions.csv should have exactly 20 rows"

    # Calculate MAE
    leaky_mae = sum(abs(t - p) for t, p in zip(test_targets, leaky_preds)) / 20.0
    fixed_mae = sum(abs(t - p) for t, p in zip(test_targets, fixed_preds)) / 20.0

    expected_leaky_str = f"Leaky MAE: {leaky_mae:.2f}"
    expected_fixed_str = f"Fixed MAE: {fixed_mae:.2f}"

    with open(metrics_txt, "r") as f:
        metrics_content = f.read().strip().split("\n")

    assert len(metrics_content) >= 2, "metrics.txt must contain at least two lines"

    assert metrics_content[0].strip() == expected_leaky_str, (
        f"First line of metrics.txt is incorrect. "
        f"Expected '{expected_leaky_str}', got '{metrics_content[0].strip()}'"
    )

    assert metrics_content[1].strip() == expected_fixed_str, (
        f"Second line of metrics.txt is incorrect. "
        f"Expected '{expected_fixed_str}', got '{metrics_content[1].strip()}'"
    )

def test_compare_sh_no_python():
    """Ensure compare.sh does not use Python."""
    compare_sh = "/home/user/experiment/compare.sh"
    with open(compare_sh, "r") as f:
        content = f.read()

    assert "python" not in content.lower(), "compare.sh must not use Python to calculate MAE"