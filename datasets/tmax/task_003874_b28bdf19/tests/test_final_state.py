# test_final_state.py

import os
import re
import pytest

def test_cypher_script_exists():
    assert os.path.exists('/home/user/graph_init.cypher'), "The file /home/user/graph_init.cypher does not exist."

def test_cypher_indexes():
    with open('/home/user/graph_init.cypher', 'r') as f:
        cypher_text = f.read()

    # Check for index creation on Employee(name)
    assert re.search(r'(?i)CREATE\s+(?:INDEX|INDEX\s+IF\s+NOT\s+EXISTS)\s+(?:FOR\s+\([a-zA-Z0-9_]+\s*:\s*Employee\)\s+ON\s+\([a-zA-Z0-9_]+\.name\)|ON\s+:Employee\(name\))', cypher_text), \
        "Missing index creation for Employee on 'name' property."

    # Check for index creation on Project(title)
    assert re.search(r'(?i)CREATE\s+(?:INDEX|INDEX\s+IF\s+NOT\s+EXISTS)\s+(?:FOR\s+\([a-zA-Z0-9_]+\s*:\s*Project\)\s+ON\s+\([a-zA-Z0-9_]+\.title\)|ON\s+:Project\(title\))', cypher_text), \
        "Missing index creation for Project on 'title' property."

def test_extracted_edges_f1_score():
    try:
        with open('/home/user/graph_init.cypher', 'r') as f:
            cypher_text = f.read()
    except FileNotFoundError:
        pytest.fail("The file /home/user/graph_init.cypher does not exist.")

    pattern = r'\{name:\s*["\']([^"\']+)["\']\}\)\-\[\:([A-Z_]+)\]\-\>\([a-zA-Z]+\:[a-zA-Z]+\s*\{(?:name|title):\s*["\']([^"\']+)["\']\}\)'
    matches = re.findall(pattern, cypher_text)

    extracted_edges = set()
    for match in matches:
        src, rel, tgt = match
        extracted_edges.add((src.strip(), rel.strip(), tgt.strip()))

    ground_truth = {
        ('Alice', 'MANAGES', 'Bob'),
        ('Bob', 'WORKS_ON', 'Project Apollo'),
        ('Charlie', 'MANAGES', 'David'),
        ('David', 'WORKS_ON', 'Project Apollo'),
        ('Alice', 'MANAGES', 'Charlie'),
        ('Eve', 'WORKS_ON', 'Project Zeus'),
        ('Alice', 'MANAGES', 'Eve')
    }

    true_positives = len(extracted_edges.intersection(ground_truth))
    false_positives = len(extracted_edges - ground_truth)
    false_negatives = len(ground_truth - extracted_edges)

    if true_positives == 0:
        f1 = 0.0
    else:
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.85, f"F1 score of extracted edges is {f1:.2f}, which is below the threshold of 0.85. Extracted: {extracted_edges}"