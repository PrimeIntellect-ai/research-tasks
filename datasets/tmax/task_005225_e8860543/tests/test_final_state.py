# test_final_state.py
import os
import stat
import subprocess
import csv
import math

def test_search_script_exists_and_executable():
    path = "/home/user/search.sh"
    assert os.path.isfile(path), f"Error: {path} is missing"
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"Error: {path} is not executable"

def test_benchmark_script_exists_and_executable():
    path = "/home/user/benchmark.sh"
    assert os.path.isfile(path), f"Error: {path} is missing"
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"Error: {path} is not executable"

def test_search_script_output():
    # Run search.sh and capture output
    cmd = ["/home/user/search.sh", "/home/user/data/query.csv", "/home/user/data/dataset.csv", "3"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"search.sh failed with error: {result.stderr}"

    actual_output = result.stdout.strip()

    # Compute expected output
    def norm(v):
        return math.sqrt(sum(x*x for x in v))

    def dot(v1, v2):
        return sum(x*y for x, y in zip(v1, v2))

    with open('/home/user/data/query.csv') as f:
        q = [float(x) for x in next(csv.reader(f))]

    docs = []
    with open('/home/user/data/dataset.csv') as f:
        for row in csv.reader(f):
            doc_id = row[0]
            v = [float(x) for x in row[1:]]
            sim = dot(q, v) / (norm(q) * norm(v))
            docs.append((doc_id, sim))

    # Sort descending, preserve original order on tie (python's sort is stable)
    docs.sort(key=lambda x: x[1], reverse=True)
    top_3 = docs[:3]

    expected_output = "\n".join([f"{d[0]},{d[1]:.4f}" for d in top_3])

    assert actual_output == expected_output, f"Mismatch!\nExpected:\n{expected_output}\nActual:\n{actual_output}"

def test_benchmark_script_execution_and_output():
    # Run benchmark.sh
    cmd = ["/home/user/benchmark.sh", "/home/user/data/query.csv", "/home/user/data/dataset.csv"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"benchmark.sh failed with error: {result.stderr}"

    results_path = "/home/user/benchmark_results.csv"
    assert os.path.isfile(results_path), f"Error: {results_path} not found"

    with open(results_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Error: {results_path} should have exactly 5 lines, found {len(lines)}"

    expected_lines = ["100", "200", "300", "400", "500"]
    for i, line in enumerate(lines):
        parts = line.split(',')
        assert len(parts) == 2, f"Error: Line {i+1} in {results_path} is not properly comma-separated"
        assert parts[0] == expected_lines[i], f"Error: Expected line {i+1} to start with {expected_lines[i]}, got {parts[0]}"
        try:
            float(parts[1])
        except ValueError:
            pytest.fail(f"Error: Execution time '{parts[1]}' on line {i+1} is not a valid float")