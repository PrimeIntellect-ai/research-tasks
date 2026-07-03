# test_final_state.py

import os
import json
import subprocess
import tempfile

def test_venv_exists():
    """Check if the virtual environment is created and python is available."""
    python_path = "/home/user/sim_env/bin/python"
    assert os.path.exists(python_path), f"Virtual environment python not found at {python_path}"
    assert os.access(python_path, os.X_OK), f"Python binary at {python_path} is not executable"

def test_fasta_file():
    """Check if the FASTA file exists and has the correct sequences."""
    fasta_path = "/home/user/data/sequences.fasta"
    assert os.path.exists(fasta_path), f"FASTA file not found at {fasta_path}"

    with open(fasta_path, "r") as f:
        content = f.read().strip()

    expected_content = ">Seq1\nATGCATGCAT\n>Seq2\nGCATGCATGC\n>Seq3\nCGATCGATCG\n>Seq4\nATATATATAT\n>Seq5\nCGCGCGCGCG"
    # Allow some flexibility with newlines
    assert content.replace("\r\n", "\n") == expected_content, "FASTA file content does not match the expected sequences."

def test_analysis_output():
    """Verify the analysis_output.json file contains the correct values."""
    output_path = "/home/user/analysis_output.json"
    assert os.path.exists(output_path), f"Output JSON not found at {output_path}"

    with open(output_path, "r") as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            assert False, "Output file is not valid JSON."

    assert "top_singular_value" in agent_data, "Missing 'top_singular_value' in JSON output."
    assert "js_distance" in agent_data, "Missing 'js_distance' in JSON output."

    # Use the student's virtual environment to compute the exact truth values
    # since we are restricted to standard library in the pytest environment.
    python_path = "/home/user/sim_env/bin/python"

    truth_script = """
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.spatial.distance import jensenshannon

sequences = [
    "ATGCATGCAT",
    "GCATGCATGC",
    "CGATCGATCG",
    "ATATATATAT",
    "CGCGCGCGCG"
]

bases = ['A', 'C', 'G', 'T']
kmers = [b1+b2 for b1 in bases for b2 in bases]
kmer_idx = {k: i for i, k in enumerate(kmers)}

vectors = []
for seq in sequences:
    vec = np.zeros(16)
    for i in range(len(seq)-1):
        kmer = seq[i:i+2]
        vec[kmer_idx[kmer]] += 1
    vectors.append(vec)

vectors = np.array(vectors)
M = np.dot(vectors, vectors.T)

U, S, Vt = np.linalg.svd(M)
top_sv = S[0]

S_trunc = np.zeros_like(S)
S_trunc[:2] = S[:2]
M_tilde = U @ np.diag(S_trunc) @ Vt

def ode_system(t, x):
    return 0.05 * np.dot(M_tilde, x) - 0.1 * x

x0 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
sol = solve_ivp(ode_system, [0, 10], x0, method='RK45')

x_final = sol.y[:, -1]

e_x = np.exp(x_final - np.max(x_final))
P = e_x / e_x.sum()

Q = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
js_dist = jensenshannon(P, Q, base=np.e)

print(json.dumps({
    "top_singular_value": round(top_sv, 4),
    "js_distance": round(js_dist, 4)
}))
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(truth_script)
        script_path = f.name

    try:
        result = subprocess.run([python_path, script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to run truth script using venv python. Error: {result.stderr}. Are numpy and scipy installed?"

        truth_data = json.loads(result.stdout.strip())
    finally:
        os.remove(script_path)

    # Compare student output to truth
    assert abs(agent_data["top_singular_value"] - truth_data["top_singular_value"]) < 1e-3, \
        f"top_singular_value mismatch. Expected ~{truth_data['top_singular_value']}, got {agent_data['top_singular_value']}"

    assert abs(agent_data["js_distance"] - truth_data["js_distance"]) < 1e-3, \
        f"js_distance mismatch. Expected ~{truth_data['js_distance']}, got {agent_data['js_distance']}"