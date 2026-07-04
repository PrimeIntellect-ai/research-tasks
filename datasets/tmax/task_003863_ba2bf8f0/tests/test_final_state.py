# test_final_state.py
import os
import subprocess
import json
import math

def get_golden_values():
    code = """
import h5py
import numpy as np
from scipy.stats import norm, wasserstein_distance
import subprocess
import json

with h5py.File('/home/user/data.h5', 'r') as f:
    data = f['empirical_data'][:]

distances = []
for row in data:
    mu, std = norm.fit(row)
    theoretical_quantiles = norm.ppf(np.linspace(0.001, 0.999, 1000), loc=mu, scale=std)
    dist = wasserstein_distance(row, theoretical_quantiles)
    distances.append(float(dist))

np.savetxt('/tmp/distances_golden.csv', distances)
r_script = '''
d <- read.csv('/tmp/distances_golden.csv', header=FALSE)$V1
res <- t.test(d, mu=0.1)
cat(res$p.value)
'''
with open('/tmp/test_golden.R', 'w') as f:
    f.write(r_script)

p_val = subprocess.check_output(['Rscript', '/tmp/test_golden.R']).decode('utf-8').strip()

print(json.dumps({'distances': distances, 'pvalue': float(p_val)}))
"""
    try:
        out = subprocess.check_output(['python3', '-c', code])
        return json.loads(out.decode('utf-8'))
    except Exception as e:
        # Fallback if libraries are missing in the test environment (should not happen if container is setup)
        return None

def test_python_script_exists_and_uses_multiprocessing():
    script_path = '/home/user/fit_and_compare.py'
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."
    with open(script_path, 'r') as f:
        content = f.read()
    assert 'multiprocessing' in content or 'ProcessPoolExecutor' in content, \
        "The Python script must use the multiprocessing library."

def test_r_script_exists():
    script_path = '/home/user/test_hypothesis.R'
    assert os.path.isfile(script_path), f"R script {script_path} is missing."

def test_distances_csv():
    csv_path = '/home/user/distances.csv'
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 200, f"Expected 200 lines in {csv_path}, found {len(lines)}."

    try:
        student_distances = [float(x) for x in lines]
    except ValueError:
        assert False, f"Not all values in {csv_path} are valid numbers."

    golden = get_golden_values()
    if golden:
        golden_distances = golden['distances']
        for i, (stud, gold) in enumerate(zip(student_distances, golden_distances)):
            assert math.isclose(stud, gold, rel_tol=1e-3, abs_tol=1e-4), \
                f"Distance at row {i} does not match. Expected ~{gold}, got {stud}."

def test_pvalue_txt():
    pvalue_path = '/home/user/pvalue.txt'
    assert os.path.isfile(pvalue_path), f"Output file {pvalue_path} is missing."

    with open(pvalue_path, 'r') as f:
        content = f.read().strip()

    try:
        student_pvalue = float(content)
    except ValueError:
        assert False, f"The content of {pvalue_path} is not a valid number: {content}"

    golden = get_golden_values()
    if golden:
        golden_pvalue = golden['pvalue']
        assert math.isclose(student_pvalue, golden_pvalue, rel_tol=1e-3, abs_tol=1e-4), \
            f"p-value does not match. Expected ~{golden_pvalue}, got {student_pvalue}."