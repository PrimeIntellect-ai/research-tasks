# test_final_state.py
import os
import json
import subprocess
import pytest

def get_golden_trace():
    script = """
import numpy as np
np.random.seed(42)
t = np.linspace(0, 1, 100)
signals = np.sin(2 * np.pi * 10 * t) + 0.1 * np.random.randn(50, 100)
F = np.fft.fft(signals, axis=1)
F[:, 20:-20] = 0
filtered = np.real(np.fft.ifft(F, axis=1))
C = np.cov(filtered)
L = np.linalg.cholesky(C + 1e-5 * np.eye(C.shape[0]))
print(np.trace(L))
"""
    try:
        output = subprocess.check_output(['python3', '-c', script], text=True)
        return float(output.strip())
    except Exception as e:
        pytest.fail(f"Failed to compute golden trace: {e}")

def test_trace_file_exists_and_correct():
    trace_file = '/home/user/trace.txt'
    assert os.path.isfile(trace_file), f"The file {trace_file} was not generated."

    with open(trace_file, 'r') as f:
        content = f.read().strip()

    assert content, f"The file {trace_file} is empty."

    try:
        trace_val = float(content)
    except ValueError:
        pytest.fail(f"The content of {trace_file} is not a valid float: {content}")

    golden_val = get_golden_trace()

    assert abs(trace_val - golden_val) < 1e-4, (
        f"The trace value in {trace_file} ({trace_val}) does not match the expected "
        f"regularized trace value (approx {golden_val})."
    )

def test_notebook_executed_successfully():
    nb_file = '/home/user/simulation.ipynb'
    assert os.path.isfile(nb_file), f"Notebook file {nb_file} is missing."

    with open(nb_file, 'r') as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Notebook file {nb_file} is not valid JSON.")

    code_cells = [c for c in nb.get('cells', []) if c.get('cell_type') == 'code']
    assert len(code_cells) > 0, "No code cells found in the notebook."

    for i, cell in enumerate(code_cells):
        assert cell.get('execution_count') is not None, f"Code cell {i+1} was not executed (execution_count is null)."
        for output in cell.get('outputs', []):
            if output.get('output_type') == 'error':
                ename = output.get('ename', 'UnknownError')
                evalue = output.get('evalue', '')
                pytest.fail(f"Notebook execution resulted in an error in cell {i+1}: {ename} - {evalue}")