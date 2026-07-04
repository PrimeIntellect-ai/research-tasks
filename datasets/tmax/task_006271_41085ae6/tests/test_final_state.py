# test_final_state.py
import os
import math
import subprocess

class LCG:
    def __init__(self, seed):
        self.state = seed
    def next_rand(self):
        self.state = (self.state * 1103515245 + 12345) % 2147483648
        return self.state / 2147483648.0

def run_integral(Nc, Nf, seed):
    rng = LCG(seed)

    x_points = []
    for i in range(Nc):
        x_points.append(0.0 + i * (0.4 / Nc))
    for i in range(Nf):
        x_points.append(0.4 + i * (0.2 / Nf))
    for i in range(Nc + 1):
        x_points.append(0.6 + i * (0.4 / Nc))

    y_points = []
    for x in x_points:
        noise = (rng.next_rand() * 0.1) - 0.05
        y = math.exp(-100 * (x - 0.5)**2) + noise
        y_points.append(y)

    integral = 0.0
    for i in range(len(x_points) - 1):
        dx = x_points[i+1] - x_points[i]
        integral += (y_points[i] + y_points[i+1]) / 2.0 * dx

    return integral

def get_expected_ci():
    results = []
    for seed in range(1, 51):
        results.append(run_integral(10, 50, seed))

    rng_boot = LCG(42)
    boot_means = []
    for b in range(1000):
        total = 0.0
        for _ in range(50):
            idx = int(rng_boot.next_rand() * 50)
            total += results[idx]
        boot_means.append(total / 50.0)

    boot_means.sort()
    lower = boot_means[24]
    upper = boot_means[974]

    return f"[{lower:.6f}, {upper:.6f}]"

def test_pipeline_execution():
    """Run pipeline.sh and verify it produces the correct bootstrap_ci.txt."""
    pipeline_path = "/home/user/pipeline.sh"
    output_file = "/home/user/bootstrap_ci.txt"

    assert os.path.exists(pipeline_path), f"{pipeline_path} does not exist."
    assert os.access(pipeline_path, os.X_OK), f"{pipeline_path} is not executable."

    # Remove output file if it exists to ensure pipeline.sh actually creates it
    if os.path.exists(output_file):
        os.remove(output_file)

    result = subprocess.run([pipeline_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.exists(output_file), f"{output_file} was not created by pipeline.sh."

    with open(output_file, 'r') as f:
        content = f.read().strip()

    expected_content = get_expected_ci()
    assert content == expected_content, f"Expected content '{expected_content}', but got '{content}' in {output_file}."