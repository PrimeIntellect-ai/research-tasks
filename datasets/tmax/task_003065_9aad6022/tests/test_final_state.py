# test_final_state.py
import os
import struct
import math

def test_c_file_exists_and_openmp():
    path = "/home/user/process_spectra.c"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "#pragma omp" in content, "OpenMP pragma (#pragma omp) missing in C code."

def test_executable_exists():
    path = "/home/user/process_spectra"
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_python_script_exists():
    path = "/home/user/plot_energies.py"
    assert os.path.exists(path), f"Python script {path} does not exist."

def test_png_exists():
    path = "/home/user/energies_plot.png"
    assert os.path.exists(path), f"Plot image {path} does not exist."

def test_energies_csv():
    csv_path = "/home/user/energies.csv"
    assert os.path.exists(csv_path), f"CSV file {csv_path} does not exist."

    spectra_path = "/home/user/spectra.dat"
    assert os.path.exists(spectra_path), f"Data file {spectra_path} does not exist."

    with open(spectra_path, "rb") as f:
        data = f.read()

    N = 1000
    M = 2048
    assert len(data) == N * M * 8, "spectra.dat size is incorrect."

    # Compute expected energies
    expected_energies = []
    for i in range(N):
        offset = i * M * 8
        signal_bytes = data[offset:offset + M * 8]
        signal = struct.unpack(f"{M}d", signal_bytes)

        energy = 0.0
        for j in range(M):
            w = 0.5 * (1.0 - math.cos(2.0 * math.pi * j / (M - 1)))
            xw = signal[j] * w
            energy += xw * xw
        expected_energies.append(energy)

    with open(csv_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == N + 1, f"CSV should have 1001 lines (header + 1000 data rows), found {len(lines)}."
    assert lines[0].strip() == "Signal_ID,Energy", f"CSV header mismatch. Expected 'Signal_ID,Energy', got '{lines[0].strip()}'."

    for i in range(N):
        parts = lines[i+1].strip().split(',')
        assert len(parts) == 2, f"CSV format error on line {i+2}: {lines[i+1]}"
        assert int(parts[0]) == i, f"Signal_ID mismatch on line {i+2}. Expected {i}, got {parts[0]}."

        actual_energy = float(parts[1])
        expected_energy = expected_energies[i]

        # Check within a reasonable tolerance for formatting string %.6f
        assert math.isclose(actual_energy, expected_energy, rel_tol=1e-5), \
            f"Energy mismatch at Signal_ID {i}: expected {expected_energy:.6f}, got {actual_energy:.6f}."