# test_final_state.py

import os
import pytest

def compare_versions(v1, v2):
    p1 = list(map(int, v1.split('.')))
    p2 = list(map(int, v2.split('.')))
    for i in range(3):
        if p1[i] > p2[i]: return 1
        if p1[i] < p2[i]: return -1
    return 0

def evaluate_condition(actual_ver, operator, target_ver):
    cmp = compare_versions(actual_ver, target_ver)
    if operator == '==': return cmp == 0
    if operator == '>=': return cmp >= 0
    if operator == '<=': return cmp <= 0
    return False

def evaluate_expression(actual_ver, expr):
    parts = [p.strip() for p in expr.split('&&')]
    for part in parts:
        tokens = part.split(' ')
        if len(tokens) == 2:
            op, target = tokens
            if not evaluate_condition(actual_ver, op, target):
                return False
    return True

@pytest.fixture(scope="module")
def expected_state():
    manifest_path = "/home/user/project/manifest.txt"
    packages_dir = "/home/user/project/packages"

    expected_report_lines = []
    expected_artifacts = []
    unexpected_artifacts = []

    if not os.path.exists(manifest_path):
        return [], [], []

    with open(manifest_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Extract package name and expression
            first_space = line.find(' ')
            if first_space == -1:
                continue

            pkg_name = line[:first_space]
            expr = line[first_space+1:].strip()

            pkg_dir = os.path.join(packages_dir, pkg_name)
            version_file = os.path.join(pkg_dir, "version.txt")
            artifact_file = os.path.join(pkg_dir, "out.artifact")

            if not os.path.exists(pkg_dir) or not os.path.exists(version_file):
                expected_report_lines.append(f"FAIL: {pkg_name} (missing)")
                unexpected_artifacts.append(artifact_file)
            else:
                with open(version_file, 'r') as vf:
                    actual_ver = vf.read().strip()

                if evaluate_expression(actual_ver, expr):
                    expected_report_lines.append(f"SUCCESS: {pkg_name} {actual_ver}")
                    expected_artifacts.append(artifact_file)
                else:
                    expected_report_lines.append(f"FAIL: {pkg_name} {actual_ver} (unsatisfied)")
                    unexpected_artifacts.append(artifact_file)

    expected_report_lines.sort()
    return expected_report_lines, expected_artifacts, unexpected_artifacts

def test_orchestrator_go_exists():
    path = "/home/user/project/orchestrator.go"
    assert os.path.isfile(path), f"Missing Go orchestrator file: {path}"

def test_build_report_content(expected_state):
    expected_report_lines, _, _ = expected_state
    report_path = "/home/user/project/build_report.txt"

    assert os.path.isfile(report_path), f"Missing build report: {report_path}"

    with open(report_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_report_lines, \
        f"Build report content does not match expected.\nExpected: {expected_report_lines}\nActual: {actual_lines}"

def test_artifacts_created(expected_state):
    _, expected_artifacts, unexpected_artifacts = expected_state

    for artifact in expected_artifacts:
        assert os.path.isfile(artifact), f"Expected artifact missing, meaning build script was not run for satisfied package: {artifact}"

    for artifact in unexpected_artifacts:
        assert not os.path.exists(artifact), f"Unexpected artifact found, meaning build script was run for unsatisfied/missing package: {artifact}"