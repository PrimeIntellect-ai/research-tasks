# test_final_state.py

import os
import json
import subprocess
import pytest
from collections import defaultdict

def test_networkx_fixed():
    target_file = '/app/networkx-3.0/networkx/readwrite/json_graph/node_link.py'
    assert os.path.isfile(target_file), f"File {target_file} is missing."

    with open(target_file, 'r') as f:
        content = f.read()

    assert 'source="src_bad"' not in content, "The deliberate perturbation source=\"src_bad\" is still present in node_link.py."

def test_detector_clean_corpus():
    detector_script = '/home/user/detector.py'
    assert os.path.isfile(detector_script), f"Detector script {detector_script} is missing."

    clean_dir = '/app/corpus/clean/'
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for fpath in clean_files:
        result = subprocess.run(['python3', detector_script, fpath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected). Offending files: {', '.join(failed_files)}")

def test_detector_evil_corpus():
    detector_script = '/home/user/detector.py'
    assert os.path.isfile(detector_script), f"Detector script {detector_script} is missing."

    evil_dir = '/app/corpus/evil/'
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for fpath in evil_files:
        result = subprocess.run(['python3', detector_script, fpath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(fpath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed (accepted). Offending files: {', '.join(failed_files)}")

def test_top_nodes_json():
    output_file = '/home/user/top_nodes.json'
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, 'r') as f:
        try:
            student_output = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_file} is not valid JSON.")

    graph_file = '/app/data/graph.json'
    assert os.path.isfile(graph_file), f"Graph data file {graph_file} is missing."

    with open(graph_file, 'r') as f:
        graph_data = json.load(f)

    # Calculate expected degrees
    degrees = defaultdict(int)
    nodes = set()

    for node in graph_data.get('nodes', []):
        node_id = node.get('id')
        if node_id is not None:
            nodes.add(node_id)

    for link in graph_data.get('links', []):
        source = link.get('source')
        target = link.get('target')
        if source is not None and target is not None:
            degrees[source] += 1
            degrees[target] += 1
            nodes.add(source)
            nodes.add(target)

    # Ensure all nodes are present in degrees even if degree is 0
    for n in nodes:
        if n not in degrees:
            degrees[n] = 0

    # Sort: degree descending, node ID ascending
    sorted_nodes = sorted(degrees.items(), key=lambda x: (-x[1], str(x[0])))

    # Get top 5
    top_5 = sorted_nodes[:5]
    expected_output = [{"id": n, "degree": d} for n, d in top_5]

    assert student_output == expected_output, f"Student output {student_output} does not match expected output {expected_output}."