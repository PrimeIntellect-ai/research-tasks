# test_final_state.py
import os
import subprocess
import json
import math
import pytest

def get_truth():
    raw = subprocess.check_output(['/app/fetch_sales_graph']).decode('utf-8').strip().split('\n')
    nodes = {}
    children = {}
    for line in raw:
        if not line: continue
        emp, mgr, sales = line.split('|')
        sales = float(sales)
        nodes[emp] = sales
        if mgr not in children:
            children[mgr] = []
        children[mgr].append(emp)

    rollups = {}
    def compute(node):
        if node in rollups: return rollups[node]
        total = nodes.get(node, 0.0)
        for c in children.get(node, []):
            total += compute(c)
        rollups[node] = total
        return total

    for n in nodes:
        compute(n)
    return rollups

def test_etl_script_accuracy():
    script_path = '/home/user/etl.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    expected = get_truth()

    try:
        output = subprocess.check_output([script_path]).decode('utf-8')
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with exit code {e.returncode}: {e.output}")

    try:
        agent_data = json.loads(output)
    except json.JSONDecodeError:
        pytest.fail("Script output is not valid JSON.")

    correct = 0
    total = len(expected)
    assert total > 0, "No expected data found from /app/fetch_sales_graph."

    for item in agent_data:
        emp = item.get('employee_id')
        val = item.get('total_rollup_sales')
        if emp in expected and val is not None:
            try:
                val_float = float(val)
                if math.isclose(val_float, expected[emp], rel_tol=1e-5, abs_tol=0.01):
                    correct += 1
            except ValueError:
                pass

    accuracy = correct / total
    assert accuracy >= 0.99, f"Accuracy {accuracy:.4f} is below the 0.99 threshold. Correct: {correct}, Total: {total}."