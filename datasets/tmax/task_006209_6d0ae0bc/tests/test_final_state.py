# test_final_state.py

import os
import sys
import importlib.util
import subprocess
import pstats

def test_integrator_fixed():
    integrator_path = "/home/user/integrator.py"
    assert os.path.isfile(integrator_path), f"File {integrator_path} does not exist."

    # Dynamically import the module
    spec = importlib.util.spec_from_file_location("integrator", integrator_path)
    integrator = importlib.util.module_from_spec(spec)
    sys.modules["integrator"] = integrator
    try:
        spec.loader.exec_module(integrator)
    except Exception as e:
        assert False, f"Failed to import {integrator_path}: {e}"

    assert hasattr(integrator, "adaptive_integrate"), "adaptive_integrate function missing."
    assert hasattr(integrator, "vdp_deriv"), "vdp_deriv function missing."

    try:
        times, states = integrator.adaptive_integrate(
            integrator.vdp_deriv, 0.0, [2.0, 0.0], 20.0, tol=1e-5
        )
    except RuntimeError as e:
        assert False, f"adaptive_integrate raised RuntimeError: {e}. The step-size bug might not be fixed correctly."
    except Exception as e:
        assert False, f"adaptive_integrate raised an unexpected error: {e}"

    assert len(times) < 1000, f"Integration took too many steps ({len(times)}). Expected less than 1000."
    assert times[-1] >= 20.0, f"Integration did not reach t_end. Final time: {times[-1]}"

def test_compare_script_and_mae():
    compare_path = "/home/user/compare.py"
    assert os.path.isfile(compare_path), f"Script {compare_path} does not exist."

    mae_log_path = "/home/user/mae.log"
    assert os.path.isfile(mae_log_path), f"Log file {mae_log_path} does not exist."

    with open(mae_log_path, "r") as f:
        content = f.read().strip()

    try:
        mae_value = float(content)
    except ValueError:
        assert False, f"Contents of {mae_log_path} could not be parsed as a float. Found: {content}"

    assert mae_value < 0.05, f"MAE value {mae_value} is too high. Expected < 0.05."

def test_plot_generated():
    plot_path = "/home/user/plot.png"
    assert os.path.isfile(plot_path), f"Plot file {plot_path} does not exist."

    with open(plot_path, "rb") as f:
        header = f.read(8)

    png_signature = b'\x89PNG\r\n\x1a\n'
    assert header == png_signature, f"File {plot_path} is not a valid PNG image."

def test_profile_generated():
    profile_script_path = "/home/user/profile_run.py"
    assert os.path.isfile(profile_script_path), f"Script {profile_script_path} does not exist."

    profile_path = "/home/user/profile.prof"
    assert os.path.isfile(profile_path), f"Profile output {profile_path} does not exist."

    try:
        stats = pstats.Stats(profile_path)
        assert stats.total_calls > 0, "Profile exists but appears to have recorded no calls."
    except Exception as e:
        assert False, f"Failed to load {profile_path} as a valid cProfile output: {e}"

def test_regression_test_script():
    test_script_path = "/home/user/test_integrator.py"
    assert os.path.isfile(test_script_path), f"Test script {test_script_path} does not exist."

    result = subprocess.run(
        [sys.executable, "-m", "unittest", test_script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, (
        f"unittest failed for {test_script_path}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )