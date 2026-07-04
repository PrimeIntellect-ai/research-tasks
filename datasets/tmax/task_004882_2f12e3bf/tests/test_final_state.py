# test_final_state.py
import os
import json
import xml.etree.ElementTree as ET
import pytest

SUMMARY_FILE = "/home/user/summary.json"
GRAPHML_FILE = "/home/user/top_paper_subgraph.graphml"

def test_summary_json_exists_and_valid():
    assert os.path.isfile(SUMMARY_FILE), f"Expected summary file at {SUMMARY_FILE} is missing."
    with open(SUMMARY_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {SUMMARY_FILE} is not a valid JSON.")

    assert "top_paper_id" in data, "Missing 'top_paper_id' in summary.json"
    assert "pagerank_score" in data, "Missing 'pagerank_score' in summary.json"
    assert "max_depth_to_top" in data, "Missing 'max_depth_to_top' in summary.json"

def test_summary_json_values():
    with open(SUMMARY_FILE, 'r') as f:
        data = json.load(f)

    assert data["top_paper_id"] == 7, f"Expected top_paper_id to be 7, got {data['top_paper_id']}"
    assert data["max_depth_to_top"] == 7, f"Expected max_depth_to_top to be 7, got {data['max_depth_to_top']}"

    pr_score = data["pagerank_score"]
    assert isinstance(pr_score, float), f"Expected pagerank_score to be a float, got {type(pr_score)}"
    assert abs(pr_score - 0.2804) < 0.01, f"Expected pagerank_score to be approx 0.2804, got {pr_score}"

def test_graphml_file_exists_and_valid():
    assert os.path.isfile(GRAPHML_FILE), f"Expected GraphML file at {GRAPHML_FILE} is missing."
    try:
        tree = ET.parse(GRAPHML_FILE)
    except ET.ParseError:
        pytest.fail(f"File {GRAPHML_FILE} is not a valid XML/GraphML file.")

    root = tree.getroot()

    # GraphML namespace
    ns = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

    # Check that it contains nodes
    nodes = root.findall('.//graphml:node', ns)
    if not nodes:
        # Sometimes namespace is missing or different, do a fallback search
        nodes = root.findall('.//node')

    assert len(nodes) > 0, "GraphML file does not contain any nodes."

    # Check if node 7 and 11 are in the graphml
    node_ids = [node.attrib.get('id') for node in nodes]
    assert '7' in node_ids or 7 in node_ids, "Top paper (node 7) is missing from the exported subgraph."
    assert '11' in node_ids or 11 in node_ids, "Node 11 (an ancestor) is missing from the exported subgraph."
    assert len(node_ids) == 13, f"Expected 13 nodes in the ancestor subgraph, got {len(node_ids)}"