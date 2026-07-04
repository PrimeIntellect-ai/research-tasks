# test_final_state.py

import os
import re

def test_pipeline_script():
    script_path = '/home/user/pipeline.sh'
    assert os.path.exists(script_path), f"{script_path} does not exist."
    with open(script_path, 'r') as f:
        content = f.read().lower()
    assert 'python' not in content, "Python usage is forbidden in pipeline.sh"
    assert 'perl' not in content, "Perl usage is forbidden in pipeline.sh"
    assert 'rscript' not in content, "R usage is forbidden in pipeline.sh"
    assert 'awk' in content, "Expected awk usage in pipeline.sh"

def test_result_file():
    result_file = '/home/user/result.txt'
    assert os.path.exists(result_file), f"{result_file} does not exist."

    # Compute exact trapezoidal distances from the generated files
    distances = []
    for i in range(1, 51):
        file_path = f'/home/user/sim_data/sim_{i}.csv'
        assert os.path.exists(file_path), f"{file_path} missing."
        with open(file_path, 'r') as f:
            lines = f.readlines()[1:] # skip header
            t = []
            v = []
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    t.append(float(parts[0]))
                    v.append(float(parts[1]))

        # Trapezoidal rule
        dist = 0.0
        for j in range(1, len(t)):
            dist += (t[j] - t[j-1]) * (v[j] + v[j-1]) / 2.0
        distances.append(dist)

    original_mean = sum(distances) / len(distances)

    with open(result_file, 'r') as f:
        content = f.read()

    # Parse output
    mean_match = re.search(r"Mean:\s*([0-9\.\-]+)", content)
    ci_match = re.search(r"95%\s*CI:\s*\[([0-9\.\-]+),\s*([0-9\.\-]+)\]", content)

    assert mean_match is not None, "Mean format not found in result.txt. Expected 'Mean: <value>'"
    assert ci_match is not None, "95% CI format not found in result.txt. Expected '95% CI: [<lower>, <upper>]'"

    agent_mean = float(mean_match.group(1))
    agent_lower = float(ci_match.group(1))
    agent_upper = float(ci_match.group(2))

    # Verify mean
    assert abs(agent_mean - original_mean) < 0.01, f"Expected mean ~{original_mean:.3f}, got {agent_mean}"

    # Verify bounds (approximate due to random seed differences in gawk vs mawk)
    expected_lower = original_mean - 0.16
    expected_upper = original_mean + 0.16

    assert abs(agent_lower - expected_lower) < 0.05, f"Lower bound {agent_lower} is too far from expected ~{expected_lower:.3f}"
    assert abs(agent_upper - expected_upper) < 0.05, f"Upper bound {agent_upper} is too far from expected ~{expected_upper:.3f}"