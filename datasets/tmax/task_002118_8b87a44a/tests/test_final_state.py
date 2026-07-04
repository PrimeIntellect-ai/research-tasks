# test_final_state.py

import os
import pytest
import numpy as np
import scipy.integrate as integrate
import scipy.stats as stats

def test_integral_result():
    agent_file = "/home/user/integral_result.txt"

    # 1. Check if the output file exists
    assert os.path.exists(agent_file), f"Failed: Output file not found at {agent_file}"
    assert os.path.isfile(agent_file), f"Failed: Path {agent_file} is not a file."

    # 2. Read and parse the agent's output
    try:
        with open(agent_file, "r") as f:
            content = f.read().strip()
            agent_val = float(content)
    except ValueError:
        pytest.fail(f"Failed: Could not parse output file content '{content}' as a float.")
    except Exception as e:
        pytest.fail(f"Failed: Error reading output file: {e}")

    # 3. Compute the exact analytical target
    mu = 1.0
    sigma = 0.5
    dist = stats.lognorm(s=sigma, scale=np.exp(mu))

    def integrand(x):
        return dist.pdf(x) * (x**2) * np.cos(x)

    true_val, _ = integrate.quad(integrand, 1.0, 4.0)

    # 4. Compare with threshold
    absolute_error = abs(true_val - agent_val)
    tolerance = 0.05  # Allow some variance due to KDE approximations and random sampling

    assert absolute_error <= tolerance, (
        f"Failed: Error {absolute_error:.6f} exceeds tolerance {tolerance}.\n"
        f"Target value: {true_val:.6f}\n"
        f"Agent value:  {agent_val:.6f}"
    )

def test_pipeline_script_exists():
    pipeline_file = "/home/user/pipeline.py"
    assert os.path.exists(pipeline_file), f"Failed: Pipeline script not found at {pipeline_file}"
    assert os.path.isfile(pipeline_file), f"Failed: Path {pipeline_file} is not a file."