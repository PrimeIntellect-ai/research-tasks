# test_final_state.py

import os
import pytest

def test_edges_txt_content():
    file_path = "/home/user/edges.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_edges = {
        "Raw_Climate_Data|Cleaned_Climate_Data|Filter",
        "Cleaned_Climate_Data|Regional_Aggregates|GroupBy",
        "Regional_Aggregates|Global_Aggregates|Merge",
        "Global_Aggregates|Global_Warming_Model|Train",
        "Cleaned_Climate_Data|Anomaly_Detection|Detect",
        "Anomaly_Detection|Global_Warming_Model|Feedback",
        "Raw_Climate_Data|Visualization_Dashboard|Plot",
        "Global_Aggregates|Visualization_Dashboard|Plot"
    }

    actual_edges = set(lines)

    assert len(lines) == 8, f"Expected exactly 8 lines in {file_path}, found {len(lines)}."
    assert actual_edges == expected_edges, "The contents of edges.txt do not match the expected edges."

def test_path_txt_content():
    file_path = "/home/user/path.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_path = [
        "Raw_Climate_Data",
        "Cleaned_Climate_Data",
        "Anomaly_Detection",
        "Global_Warming_Model"
    ]

    assert lines == expected_path, f"The contents of {file_path} do not match the expected shortest path."