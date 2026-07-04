# test_final_state.py
import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/sim_pipeline"
GENERATE_DATA_EXE = os.path.join(WORKSPACE_DIR, "generate_data")
DATASET_TXT = os.path.join(WORKSPACE_DIR, "dataset.txt")
OPTIMIZER_PY = os.path.join(WORKSPACE_DIR, "optimizer.py")
EVALUATE_SH = os.path.join(WORKSPACE_DIR, "evaluate.sh")
FINAL_MSE_TXT = os.path.join(WORKSPACE_DIR, "final_mse.txt")

def test_generate_data_compiled_and_run():
    assert os.path.isfile(GENERATE_DATA_EXE), f"{GENERATE_DATA_EXE} not found. Did you compile generate_data.c?"
    assert os.access(GENERATE_DATA_EXE, os.X_OK), f"{GENERATE_DATA_EXE} is not executable."

    assert os.path.isfile(DATASET_TXT), f"{DATASET_TXT} not found. Did you run the generator and redirect output?"
    with open(DATASET_TXT, 'r') as f:
        content = f.read().strip()
    assert len(content) > 0, f"{DATASET_TXT} is empty."

    for line in content.split('\n'):
        parts = line.strip().split()
        assert len(parts) == 2, f"Invalid format in dataset.txt: '{line}'"
        try:
            float(parts[0])
            float(parts[1])
        except ValueError:
            pytest.fail(f"Non-float values in dataset.txt: '{line}'")

def test_optimizer_py_cli():
    assert os.path.isfile(OPTIMIZER_PY), f"{OPTIMIZER_PY} not found."
    try:
        result = subprocess.run(
            ["python3", OPTIMIZER_PY, "100.0", "-100.0"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"optimizer.py failed to run with extreme initial conditions: {e.stderr}")

    output = result.stdout.strip()
    parts = output.split()
    assert len(parts) == 2, f"optimizer.py should print exactly two values (x y). Got: '{output}'"

    try:
        x_opt = float(parts[0])
        y_opt = float(parts[1])
    except ValueError:
        pytest.fail(f"optimizer.py output non-float values: '{output}'")

    assert abs(x_opt - 3.14) < 1e-2, f"Optimized x is too far from 3.14: {x_opt}"
    assert abs(y_opt - (-2.71)) < 1e-2, f"Optimized y is too far from -2.71: {y_opt}"

def test_evaluate_sh_exists_and_executable():
    assert os.path.isfile(EVALUATE_SH), f"{EVALUATE_SH} not found."
    assert os.access(EVALUATE_SH, os.X_OK), f"{EVALUATE_SH} is not executable. Run chmod +x."

def test_final_mse_format_and_value():
    assert os.path.isfile(FINAL_MSE_TXT), f"{FINAL_MSE_TXT} not found. Did evaluate.sh produce it?"
    with open(FINAL_MSE_TXT, 'r') as f:
        content = f.read().strip()

    assert content.startswith("MSE:"), f"Invalid format in final_mse.txt. Expected 'MSE: <value>', got: '{content}'"

    try:
        mse_str = content.split(":")[1].strip()
        mse_val = float(mse_str)
    except (IndexError, ValueError):
        pytest.fail(f"Could not parse MSE value from final_mse.txt: '{content}'")

    assert mse_val < 1e-3, f"MSE is too high ({mse_val}). Optimization failed or function wasn't stable."

def test_evaluate_sh_reproducible():
    if os.path.exists(FINAL_MSE_TXT):
        os.remove(FINAL_MSE_TXT)

    try:
        subprocess.run([EVALUATE_SH], check=True, cwd=WORKSPACE_DIR, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"evaluate.sh failed to run: {e.stderr}")

    assert os.path.isfile(FINAL_MSE_TXT), "evaluate.sh did not create final_mse.txt"

    with open(FINAL_MSE_TXT, 'r') as f:
        content = f.read().strip()

    assert content.startswith("MSE:"), "Invalid format in final_mse.txt after running evaluate.sh"
    mse_val = float(content.split(":")[1].strip())
    assert mse_val < 1e-3, f"MSE is too high after running evaluate.sh: {mse_val}"