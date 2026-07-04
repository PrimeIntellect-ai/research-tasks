# test_final_state.py

import os
import hashlib
import pytest

def evaluate_expression(expr):
    # Safe evaluation of simple math expressions
    try:
        return eval(expr, {"__builtins__": None}, {})
    except Exception:
        return None

def test_pipeline_log_content():
    expressions_file = '/home/user/data/expressions.txt'
    log_file = '/home/user/pipeline.log'

    assert os.path.exists(expressions_file), f"{expressions_file} is missing"
    assert os.path.exists(log_file), f"{log_file} is missing"

    with open(expressions_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    seen_hashes = set()
    duplicates = 0
    total_lines = len(lines)

    for expr in lines:
        val = evaluate_expression(expr)
        if val is not None:
            formatted_val = f"{val:.4f}"
            h = hashlib.md5(formatted_val.encode('utf-8')).hexdigest()
            if h in seen_hashes:
                duplicates += 1
            else:
                seen_hashes.add(h)

    expected_log = f"INFO: Processed {total_lines} lines, found {duplicates} duplicates."

    with open(log_file, 'r') as f:
        log_content = f.read().strip()

    assert expected_log in log_content, f"Expected '{expected_log}' in {log_file}, but got: {log_content}"

def test_report_content():
    expressions_file = '/home/user/data/expressions.txt'
    template_file = '/home/user/template.md'
    report_file = '/home/user/report.md'

    assert os.path.exists(expressions_file), f"{expressions_file} is missing"
    assert os.path.exists(template_file), f"{template_file} is missing"
    assert os.path.exists(report_file), f"{report_file} is missing"

    with open(expressions_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    seen_hashes = set()
    unique_expressions = []

    for expr in lines:
        val = evaluate_expression(expr)
        if val is not None:
            formatted_val = f"{val:.4f}"
            h = hashlib.md5(formatted_val.encode('utf-8')).hexdigest()
            if h not in seen_hashes:
                seen_hashes.add(h)
                unique_expressions.append(f"{expr} = {val:.1f}")

    with open(template_file, 'r') as f:
        template = f.read()

    expected_report = template.replace('{{UNIQUE_COUNT}}', str(len(unique_expressions)))
    expected_report = expected_report.replace('{{EXPRESSIONS_LIST}}', '\n'.join(unique_expressions))

    with open(report_file, 'r') as f:
        actual_report = f.read().strip()

    assert actual_report == expected_report.strip(), f"Content of {report_file} does not match the expected output based on the template."