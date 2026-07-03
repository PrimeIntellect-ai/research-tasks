# test_final_state.py

import os
import subprocess
import pytest

def test_cargo_test_passes():
    """Verify that cargo test passes in the Rust project."""
    project_dir = "/home/user/oscillator_fit"
    assert os.path.isdir(project_dir), f"{project_dir} does not exist"

    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed:\n{result.stdout}\n{result.stderr}"

def test_results_file_content():
    """Verify that results.txt contains the correct output."""
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"{results_path} does not exist"

    with open(results_path, "r") as f:
        content = f.read().strip()

    assert "c: 0.51, k: 1.98" in content, f"Expected 'c: 0.51, k: 1.98' in {results_path}, found: {content}"

def test_fit_png_exists():
    """Verify that the plot was successfully generated."""
    png_path = "/home/user/fit.png"
    assert os.path.isfile(png_path), f"{png_path} does not exist"
    assert os.path.getsize(png_path) > 0, f"{png_path} is empty"

def test_integrator_fixed():
    """Verify that the bug in integrator.rs was fixed."""
    integrator_path = "/home/user/oscillator_fit/src/integrator.rs"
    assert os.path.isfile(integrator_path), f"{integrator_path} does not exist"

    with open(integrator_path, "r") as f:
        content = f.read()

    # Check that the logic was inverted back to correct
    # The original had *dt *= 2.0 on error > tolerance
    # A correct implementation should decrease dt on high error
    assert "*dt *= 0.5" in content or "*dt /= 2.0" in content, "Step size should be halved on high error"

def test_mcmc_implemented():
    """Verify that the MCMC logic was implemented."""
    mcmc_path = "/home/user/oscillator_fit/src/mcmc.rs"
    assert os.path.isfile(mcmc_path), f"{mcmc_path} does not exist"

    with open(mcmc_path, "r") as f:
        content = f.read()

    # Check that it calculates the acceptance probability or uses rng
    assert "exp()" in content or "gen_bool" in content or "gen::<f64>()" in content, "MCMC acceptance logic seems incomplete"