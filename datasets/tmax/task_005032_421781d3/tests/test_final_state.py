# test_final_state.py

import os
import subprocess
import pytest

def test_kl_result_file():
    kl_file = "/home/user/kl_result.txt"
    assert os.path.isfile(kl_file), f"The file {kl_file} is missing. Did you write the KL divergence result to it?"

    with open(kl_file, "r") as f:
        content = f.read().strip()

    try:
        kl_value = float(content)
    except ValueError:
        pytest.fail(f"The content of {kl_file} is not a valid float: '{content}'")

    assert kl_value < 0.1, f"The KL divergence value {kl_value} is too high. The integrator fix or KL calculation might be incorrect."

def test_distribution_plot_exists():
    plot_file = "/home/user/distribution.png"
    assert os.path.isfile(plot_file), f"The plot file {plot_file} is missing. Did you generate the visualization?"
    assert os.path.getsize(plot_file) > 0, f"The plot file {plot_file} is empty."

def test_integrator_fixed():
    integrator_rs = "/home/user/langevin_fit/src/integrator.rs"
    assert os.path.isfile(integrator_rs), f"The file {integrator_rs} is missing."

    with open(integrator_rs, "r") as f:
        content = f.read()

    assert "(tolerance / err).sqrt()" in content or "(tolerance/err).sqrt()" in content, \
        "The integrator.rs file does not contain the fixed step-size formula (tolerance / err).sqrt()."

def test_cargo_test_passes():
    integration_test_rs = "/home/user/langevin_fit/tests/integration_test.rs"
    assert os.path.isfile(integration_test_rs), f"The regression test file {integration_test_rs} is missing."

    result = subprocess.run(
        ["cargo", "test"],
        cwd="/home/user/langevin_fit",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"`cargo test` failed. Output:\n{result.stdout}\n{result.stderr}"
    assert "test result: ok." in result.stdout or "1 passed" in result.stdout, "No tests passed or no tests were found."

def test_python_script_exists():
    script_file = "/home/user/plot_dist.py"
    assert os.path.isfile(script_file), f"The python script {script_file} is missing."