# test_final_state.py

import os
import json
import heapq

def evaluate_prefix(expr):
    tokens = expr.strip().split()
    stack = []
    for token in reversed(tokens):
        if token in ['ADD', 'SUB', 'MUL', 'DIV', 'XOR']:
            if len(stack) < 2:
                raise ValueError("Invalid prefix expression")
            op1 = stack.pop()
            op2 = stack.pop()
            if token == 'ADD':
                stack.append(op1 + op2)
            elif token == 'SUB':
                stack.append(op1 - op2)
            elif token == 'MUL':
                stack.append(op1 * op2)
            elif token == 'DIV':
                stack.append(op1 // op2)
            elif token == 'XOR':
                stack.append(op1 ^ op2)
        else:
            stack.append(int(token))
    if len(stack) != 1:
        raise ValueError("Invalid prefix expression")
    return stack[0]

def get_expected_results(pipeline_path):
    with open(pipeline_path, 'r') as f:
        data = json.load(f)

    in_degree = {k: 0 for k in data}
    adj = {k: [] for k in data}

    for k, v in data.items():
        for dep in v.get('deps', []):
            if dep in adj:
                adj[dep].append(k)
                in_degree[k] += 1

    pq = []
    for k, deg in in_degree.items():
        if deg == 0:
            heapq.heappush(pq, k)

    results = []
    while pq:
        curr = heapq.heappop(pq)
        val = evaluate_prefix(data[curr]['expr'])
        results.append({"step": curr, "result": val})

        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(pq, neighbor)

    return results

def test_websocket_log_correct():
    log_path = "/home/user/ws_received.log"
    pipeline_path = "/home/user/pipeline.json"

    assert os.path.exists(pipeline_path), f"Pipeline file {pipeline_path} is missing."
    assert os.path.exists(log_path), f"Log file {log_path} was not created. The script may not have run or sent messages correctly."

    expected_results = get_expected_results(pipeline_path)

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    actual_results = []
    for line in lines:
        try:
            actual_results.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Log file contains invalid JSON: {line}"

    assert len(actual_results) == len(expected_results), (
        f"Expected {len(expected_results)} messages, but found {len(actual_results)} in {log_path}. "
        f"Ensure all steps are processed."
    )

    for i, (act, exp) in enumerate(zip(actual_results, expected_results)):
        assert act == exp, (
            f"Message mismatch at step {i + 1} (0-indexed {i}).\n"
            f"Expected: {exp}\n"
            f"Actual:   {act}\n"
            f"Check your topological sort logic and expression evaluator."
        )