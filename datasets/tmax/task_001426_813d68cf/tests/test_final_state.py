# test_final_state.py

import os
import urllib.request
import urllib.error
import difflib
import ast
import operator

def test_evaluator_c_exists():
    """Check if /home/user/evaluator.c exists."""
    assert os.path.isfile("/home/user/evaluator.c"), "/home/user/evaluator.c is missing."

def _eval_expr(expr):
    """Safely evaluate a mathematical expression string with +, *, and ()."""
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Mult):
                return left * right
            else:
                raise ValueError(f"Unsupported operator: {node.op}")
        elif isinstance(node, ast.Expression):
            return _eval(node.body)
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")

    return _eval(ast.parse(expr, mode='eval'))

def test_costs_v2_content():
    """Check if /home/user/costs_v2.txt contains the correct evaluated costs."""
    formulas_path = "/home/user/formulas_v2.txt"
    costs_v2_path = "/home/user/costs_v2.txt"

    assert os.path.isfile(formulas_path), f"{formulas_path} is missing."
    assert os.path.isfile(costs_v2_path), f"{costs_v2_path} is missing."

    expected_lines = set()
    with open(formulas_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue

            try:
                mod_expr, checksum_str = line.split('|')
                mod_str, expr_str = mod_expr.split(':', 1)

                mod = mod_str.strip()
                expr = expr_str.strip()
                checksum = int(checksum_str.strip())

                # Calculate XOR checksum
                calc_checksum = 0
                for c in expr:
                    calc_checksum ^= ord(c)

                if calc_checksum == checksum:
                    cost = _eval_expr(expr)
                    expected_lines.add(f"{mod}: {cost}")
            except Exception:
                pass

    with open(costs_v2_path, 'r') as f:
        actual_lines = set(line.strip() for line in f if line.strip())

    assert expected_lines == actual_lines, f"Expected {expected_lines} in costs_v2.txt, got {actual_lines}"

def test_cost_diff_content():
    """Check if /home/user/cost_diff.txt contains the correct unified diff."""
    v1_path = "/home/user/costs_v1.txt"
    v2_path = "/home/user/costs_v2.txt"
    diff_path = "/home/user/cost_diff.txt"

    assert os.path.isfile(diff_path), f"{diff_path} is missing."

    with open(v1_path, 'r') as f:
        v1_lines = sorted([line.strip() for line in f if line.strip()])
    with open(v2_path, 'r') as f:
        v2_lines = sorted([line.strip() for line in f if line.strip()])

    expected_diff = list(difflib.unified_diff(
        v1_lines, v2_lines,
        fromfile=v1_path, tofile=v2_path,
        lineterm=''
    ))

    expected_changes = [line for line in expected_diff if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))]

    with open(diff_path, 'r') as f:
        actual_diff_lines = [line.strip() for line in f]

    actual_changes = [line for line in actual_diff_lines if line.startswith(('+', '-')) and not line.startswith(('+++', '---'))]

    assert expected_changes == actual_changes, "The additions and deletions in the diff do not match the expected changes."

def test_proxy_server_diff():
    """Check if the proxy server returns the correct diff on /ci/diff."""
    diff_path = "/home/user/cost_diff.txt"
    assert os.path.isfile(diff_path), f"{diff_path} is missing."

    with open(diff_path, 'rb') as f:
        expected_content = f.read()

    try:
        req = urllib.request.Request("http://localhost:8080/ci/diff")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            actual_content = response.read()
            assert actual_content == expected_content, "Proxy did not return the exact contents of cost_diff.txt"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to proxy server or error occurred: {e}"

def test_proxy_server_404():
    """Check if the proxy server returns 404 for unknown paths."""
    try:
        req = urllib.request.Request("http://localhost:8080/other")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert False, "Expected HTTP Error 404, but request succeeded."
    except urllib.error.HTTPError as e:
        assert e.code == 404, f"Expected HTTP Error 404, got {e.code}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to proxy server: {e}"