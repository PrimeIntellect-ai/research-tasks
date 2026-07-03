# test_final_state.py
import os
import stat
import pytest

def test_run_pipeline_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Missing file: {path}"
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"File {path} is not executable"

def test_summary_csv():
    path = "/home/user/summary.csv"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 3, f"Expected at least 3 lines in {path} (header + 2 groups), found {len(lines)}"
    assert lines[0] == "server_group,avg_latency", f"Incorrect header in {path}: {lines[0]}"

    data_lines = set(lines[1:])
    expected_lines = {"A,101.26", "B,114.20"}
    assert expected_lines.issubset(data_lines), f"Expected data {expected_lines} not found in {path}. Found: {data_lines}"

def test_p_value_txt():
    path = "/home/user/p_value.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "0.0001", f"Expected p-value '0.0001' in {path}, found '{content}'"

def test_latency_plot_png():
    path = "/home/user/latency_plot.png"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, 'rb') as f:
        magic = f.read(4)

    assert magic == b'\x89PNG', f"File {path} is not a valid PNG file (invalid magic bytes)"