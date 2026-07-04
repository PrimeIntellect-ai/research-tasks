# test_final_state.py

import os
import subprocess
import importlib

def test_dependencies_installed():
    """Test that required Python packages are installed."""
    missing = []
    for pkg in ['mpi4py', 'scipy', 'matplotlib']:
        try:
            importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
    assert not missing, f"Missing required Python packages: {', '.join(missing)}"

def test_metric_file():
    """Test that metric.txt exists and contains a valid float."""
    metric_path = "/home/user/metric.txt"
    assert os.path.isfile(metric_path), f"{metric_path} does not exist."

    with open(metric_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"{metric_path} does not contain a valid floating-point number. Content: {content}"

    assert val >= 0, "Wasserstein distance should be non-negative."

def test_visualization_exists():
    """Test that visualization.png exists and is a valid PNG image."""
    img_path = "/home/user/visualization.png"
    assert os.path.isfile(img_path), f"{img_path} does not exist."

    with open(img_path, "rb") as f:
        header = f.read(8)

    # PNG magic number: \x89PNG\r\n\x1a\n
    assert header == b'\x89PNG\r\n\x1a\n', f"{img_path} is not a valid PNG file."

def test_fix_sim_reproducibility():
    """Test that fix_sim.py produces process-count-invariant results."""
    fix_sim_path = "/home/user/fix_sim.py"
    assert os.path.isfile(fix_sim_path), f"{fix_sim_path} does not exist."

    seed = "100"

    def run_sim(procs):
        cmd = ["mpirun", "--allow-run-as-root", "-n", str(procs), "python3", fix_sim_path, seed]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Running fix_sim.py with {procs} processes failed:\n{result.stderr}"
        return result.stdout.strip()

    res_1 = run_sim(1)
    res_4 = run_sim(4)

    assert res_1, "Output from fix_sim.py (1 process) is empty."
    assert res_1 == res_4, f"Output mismatch! 1 process: {res_1}, 4 processes: {res_4}"