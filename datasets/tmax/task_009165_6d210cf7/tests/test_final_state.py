# test_final_state.py
import os

def test_run_sh_exists_and_executable():
    """Check if /home/user/run.sh exists and is executable."""
    file_path = '/home/user/run.sh'
    assert os.path.isfile(file_path), f"{file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"{file_path} is not executable."

def test_train_model_exists():
    """Check if /home/user/train_model.py exists."""
    file_path = '/home/user/train_model.py'
    assert os.path.isfile(file_path), f"{file_path} does not exist."

def test_sim_txt_value():
    """Check if /home/user/sim.txt contains the correct value."""
    file_path = '/home/user/sim.txt'
    assert os.path.isfile(file_path), f"{file_path} does not exist. Did the script run successfully?"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    try:
        sim_val = float(content)
    except ValueError:
        assert False, f"{file_path} does not contain a valid float. Found: '{content}'"

    # The expected value is approximately 0.3847
    expected_sim = 0.3847
    assert abs(sim_val - expected_sim) < 0.001, f"Expected similarity ~{expected_sim}, but got {sim_val}"

def test_metrics_txt_value():
    """Check if /home/user/metrics.txt contains the correct accuracy."""
    file_path = '/home/user/metrics.txt'
    assert os.path.isfile(file_path), f"{file_path} does not exist. Did the script run successfully?"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    try:
        acc_val = float(content)
    except ValueError:
        assert False, f"{file_path} does not contain a valid float. Found: '{content}'"

    # The expected accuracy is 1.0000
    expected_acc = 1.0
    assert abs(acc_val - expected_acc) < 0.001, f"Expected accuracy ~{expected_acc}, but got {acc_val}"