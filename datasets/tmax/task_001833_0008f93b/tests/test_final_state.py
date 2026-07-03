# test_final_state.py

import os
import subprocess

def test_source_code_exists():
    assert os.path.isfile("/home/user/spectromark.cpp"), "C++ source code /home/user/spectromark.cpp is missing."

def test_compiled_binary_exists_and_is_elf():
    binary_path = "/home/user/spectromark"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    with open(binary_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{binary_path} is not a valid ELF binary."

def test_hdf5_file_exists_and_valid():
    h5_path = "/home/user/spectra.h5"
    assert os.path.isfile(h5_path), f"HDF5 file {h5_path} is missing."

    # Check HDF5 magic number
    with open(h5_path, "rb") as f:
        magic = f.read(8)
    assert magic == b"\x89HDF\x0d\x0a\x1a\x0a", f"{h5_path} is not a valid HDF5 file."

    # Check dataset structure using h5ls if available
    if os.system("command -v h5ls > /dev/null") == 0:
        result = subprocess.run(["h5ls", h5_path], capture_output=True, text=True)
        assert "raw_data" in result.stdout and "1000, 500" in result.stdout, "Dataset 'raw_data' of size 1000x500 not found in HDF5 file."

def test_svd_results_correctness():
    txt_path = "/home/user/svd_results.txt"
    assert os.path.isfile(txt_path), f"SVD results file {txt_path} is missing."

    with open(txt_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines in {txt_path}, found {len(lines)}."

    values = []
    for line in lines:
        try:
            values.append(float(line))
        except ValueError:
            assert False, f"Could not parse '{line}' as a float in {txt_path}."

    # Check descending order
    assert values == sorted(values, reverse=True), "Singular values are not in descending order."

    # First singular value should be roughly between 400 and 700 based on the math
    assert 400 < values[0] < 700, f"First singular value {values[0]} is out of expected range (400-700)."

def test_callgrind_output_exists():
    cg_path = "/home/user/callgrind.out"
    assert os.path.isfile(cg_path), f"Callgrind output file {cg_path} is missing."
    assert os.path.getsize(cg_path) > 0, f"Callgrind output file {cg_path} is empty."

    with open(cg_path, "r", errors="ignore") as f:
        content = f.read(1024)
    assert "creator: callgrind" in content.lower() or "events:" in content.lower() or "positions:" in content.lower(), "File does not appear to be a valid callgrind output."

def test_visualization_script_exists():
    py_path = "/home/user/plot_svd.py"
    assert os.path.isfile(py_path), f"Python visualization script {py_path} is missing."

def test_plot_image_exists_and_is_png():
    png_path = "/home/user/svd_plot.png"
    assert os.path.isfile(png_path), f"Plot image {png_path} is missing."

    with open(png_path, "rb") as f:
        magic = f.read(8)
    assert magic == b"\x89PNG\x0d\x0a\x1a\x0a", f"{png_path} is not a valid PNG image."