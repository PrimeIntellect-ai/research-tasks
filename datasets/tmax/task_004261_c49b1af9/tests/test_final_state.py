# test_final_state.py
import os
import math
import pytest

def get_truth():
    lengths = []
    gc_counts = []
    with open('/app/data.fasta', 'r') as f:
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    lengths.append(len(seq))
                    gc_counts.append(seq.count('G') + seq.count('C'))
                seq = ""
            else:
                seq += line
        if seq:
            lengths.append(len(seq))
            gc_counts.append(seq.count('G') + seq.count('C'))

    n = len(lengths)
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if abs(lengths[i] - lengths[j]) <= 2:
                adj[i].append(j)
                adj[j].append(i)

    visited = set()
    components = []
    for i in range(n):
        if i not in visited:
            comp = []
            q = [i]
            visited.add(i)
            while q:
                curr = q.pop(0)
                comp.append(curr)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        q.append(neighbor)
            components.append(comp)

    lcc = max(components, key=len)

    x = [lengths[i] for i in lcc]
    y = [gc_counts[i] for i in lcc]

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x)**2 for xi in x)
    den_y = sum((yi - mean_y)**2 for yi in y)

    r = num / math.sqrt(den_x * den_y)

    N = len(lcc)
    t = r * math.sqrt(N - 2) / math.sqrt(1 - r**2)
    return abs(t)

def test_result_exists_and_correct():
    result_path = '/app/result.txt'
    assert os.path.isfile(result_path), f"Expected output file {result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        agent_val = float(content)
    except ValueError:
        pytest.fail(f"Content of {result_path} is not a valid float: '{content}'")

    target_val = get_truth()
    error = abs(agent_val - target_val)

    assert error <= 0.01, (
        f"Computed statistic is incorrect. "
        f"Agent value: {agent_val}, Target value: {target_val}, "
        f"Absolute error: {error} (Threshold: <= 0.01)"
    )