# test_final_state.py

import os
import json
import sys
import subprocess
import pytest

def get_expected_results():
    script = """
import torch
import json

torch.manual_seed(42)
a = torch.randn(1, requires_grad=True, dtype=torch.float32)
b = torch.randn(1, requires_grad=True, dtype=torch.float32)
c = torch.randn(1, requires_grad=True, dtype=torch.float32)

# Hardcoded dataset from the prompt to avoid needing pandas in the test evaluation if it was uninstalled
x = torch.tensor([-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0], dtype=torch.float32)
y = torch.tensor([-4.5, -4.8, -2.5, 1.1, 4.6, 6.9, 7.6], dtype=torch.float32)

criterion = torch.nn.MSELoss()
optimizer = torch.optim.SGD([a, b, c], lr=0.05)

for epoch in range(500):
    optimizer.zero_grad()
    y_pred = a * torch.sin(x) + b * x + c
    loss = criterion(y_pred, y)
    loss.backward()
    optimizer.step()

print(json.dumps({
    "a": round(a.item(), 4),
    "b": round(b.item(), 4),
    "c": round(c.item(), 4),
    "final_loss": round(loss.item(), 4)
}))
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Failed to compute expected results using PyTorch. Is PyTorch installed? Error: {result.stderr}")

    return json.loads(result.stdout)

def test_results_json_exists_and_correct():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Expected results file {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            student_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected_results = get_expected_results()

    expected_keys = {"a", "b", "c", "final_loss"}
    assert set(student_results.keys()) == expected_keys, f"JSON keys in {results_path} do not match expected keys. Expected {expected_keys}, got {set(student_results.keys())}"

    for key in expected_keys:
        student_val = student_results[key]
        expected_val = expected_results[key]

        assert isinstance(student_val, (int, float)), f"Value for '{key}' must be a number."

        # Allow a tiny bit of floating point tolerance due to potential minor platform differences, 
        # but prompt asked to round to 4 decimal places.
        assert abs(student_val - expected_val) <= 1e-3, \
            f"Value for '{key}' is incorrect. Expected {expected_val}, got {student_val}."