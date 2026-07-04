# test_final_state.py
import os
import json
import pytest

def test_notebook_exists_and_executed():
    """Test that the Jupyter notebook exists and has been executed."""
    notebook_path = "/home/user/assembly.ipynb"
    assert os.path.exists(notebook_path), f"Notebook not found at {notebook_path}"

    with open(notebook_path, 'r', encoding='utf-8') as f:
        try:
            nb_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Notebook {notebook_path} is not valid JSON.")

    executed = False
    for cell in nb_data.get('cells', []):
        if cell.get('cell_type') == 'code':
            exec_count = cell.get('execution_count')
            if exec_count is not None and isinstance(exec_count, int) and exec_count > 0:
                executed = True
                break

    assert executed, "Notebook was not executed properly (no valid execution counts found)."

def test_hub_sequence_file():
    """Test that the hub sequence file exists and contains the correct sequence."""
    hub_path = "/home/user/hub_sequence.txt"
    assert os.path.exists(hub_path), f"Hub sequence file not found at {hub_path}"

    with open(hub_path, 'r', encoding='utf-8') as f:
        hub_seq = f.read().strip()

    assert hub_seq == "AAACTAG", f"Incorrect hub sequence found: {hub_seq}. Expected 'AAACTAG'."

def test_graph_image_exists():
    """Test that the graph image file was generated."""
    graph_path = "/home/user/graph.png"
    assert os.path.exists(graph_path), f"Graph image not found at {graph_path}"
    assert os.path.getsize(graph_path) > 0, "Graph image file exists but is empty."