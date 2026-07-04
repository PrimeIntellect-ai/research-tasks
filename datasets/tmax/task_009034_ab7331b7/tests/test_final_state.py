# test_final_state.py

import os
import subprocess
import tempfile
import pytest

WORKSPACE_DIR = "/home/user/workspace"
GO_SCRIPT = os.path.join(WORKSPACE_DIR, "simulate_network.go")
OUTPUT_FILE = os.path.join(WORKSPACE_DIR, "stable_output.txt")

def get_golden_value():
    golden_go = """
package main
import "fmt"
func simulateODE(y0 float64, k float64, steps int, dt float64) float64 {
	y := y0
	for i := 0; i < steps; i++ { y -= k*y*dt }
	return y
}
func main() {
	var total float64
	for i := 1; i <= 1000; i++ {
		total += simulateODE(100.0, 0.1 + float64(i)*0.0001, 1000, 0.01)
	}
	fmt.Printf("%.15f\\n", total/1000.0)
}
"""
    with tempfile.NamedTemporaryFile(suffix=".go", mode="w", delete=False) as f:
        f.write(golden_go)
        temp_name = f.name

    try:
        result = subprocess.run(["go", "run", temp_name], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    finally:
        os.remove(temp_name)

def test_go_script_modified_correctly():
    """Verify the Go script no longer uses mutexes for summation."""
    assert os.path.isfile(GO_SCRIPT), f"File {GO_SCRIPT} does not exist."
    with open(GO_SCRIPT, 'r') as f:
        content = f.read()

    assert "mu.Lock()" not in content, "The script still contains mu.Lock(), which should have been removed."
    assert "sync.Mutex" not in content, "The script still imports/uses sync.Mutex."

def test_output_file_exists_and_correct():
    """Verify that stable_output.txt exists, has 5 lines, and matches the golden deterministic value."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} was not created."

    with open(OUTPUT_FILE, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines of output, found {len(lines)}."

    golden_val = get_golden_value()

    for i, line in enumerate(lines):
        assert line == golden_val, f"Line {i+1} does not match the expected deterministic output. Expected {golden_val}, got {line}."

def test_script_compiles_and_runs():
    """Verify that the modified script compiles and runs successfully."""
    result = subprocess.run(["go", "run", GO_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to run. Stderr: {result.stderr}"

    output = result.stdout.strip()
    golden_val = get_golden_value()
    assert output == golden_val, f"Script output {output} does not match golden value {golden_val}."