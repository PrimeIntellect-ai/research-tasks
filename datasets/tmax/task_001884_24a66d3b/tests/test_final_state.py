# test_final_state.py
import os
import stat
import pytest

def test_latency_summary_csv():
    csv_path = "/home/user/mlops_pipeline/latency_summary.csv"
    assert os.path.isfile(csv_path), f"File missing: {csv_path}"

    expected_csv = (
        "batch_size,latency_ms\n"
        "1,20\n"
        "2,32\n"
        "4,56\n"
        "8,104\n"
        "16,200\n"
    )

    with open(csv_path, "r") as f:
        content = f.read().strip()

    expected_content = expected_csv.strip()
    assert content == expected_content, f"Content of {csv_path} does not match expected output.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_artifact_plot_png():
    png_path = "/home/user/mlops_pipeline/artifact_plot.png"
    assert os.path.isfile(png_path), f"File missing: {png_path}"

    file_size = os.path.getsize(png_path)
    assert file_size > 0, f"File {png_path} is empty (0 bytes)"

    with open(png_path, "rb") as f:
        header = f.read(8)

    assert header == b"\x89PNG\r\n\x1a\n", f"File {png_path} is not a valid PNG image (invalid header)"

def test_run_experiments_script():
    script_path = "/home/user/mlops_pipeline/run_experiments.sh"
    assert os.path.isfile(script_path), f"File missing: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

    with open(script_path, "r") as f:
        content = f.read()

    assert "generate_embeddings.py" in content, f"Script {script_path} does not run generate_embeddings.py"
    assert "plot_artifacts.py" in content, f"Script {script_path} does not run plot_artifacts.py"

def test_logs_directory_and_files():
    logs_dir = "/home/user/mlops_pipeline/logs"
    assert os.path.isdir(logs_dir), f"Directory missing: {logs_dir}"

    for size in [1, 2, 4, 8, 16]:
        log_file = os.path.join(logs_dir, f"run_{size}.log")
        assert os.path.isfile(log_file), f"Log file missing: {log_file}"

        with open(log_file, "r") as f:
            content = f.read()
        assert f"Batch Size: {size}" in content, f"Log file {log_file} does not contain correct batch size"
        assert "Latency:" in content, f"Log file {log_file} does not contain latency information"