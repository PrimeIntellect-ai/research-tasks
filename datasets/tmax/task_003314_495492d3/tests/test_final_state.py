# test_final_state.py
import os
import math

RAW_FILE = "/home/user/raw_spectra.txt"
FILTERED_FILE = "/home/user/filtered_spectra.txt"
PEAKS_FILE = "/home/user/peaks.log"
PLOT_FILE = "/home/user/plot.txt"

def get_expected_data():
    assert os.path.isfile(RAW_FILE), f"Missing {RAW_FILE}"

    with open(RAW_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    wavelengths = []
    intensities = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        wavelengths.append(int(parts[0]))
        intensities.append(float(parts[1]))

    n = len(intensities)
    filtered = []

    for i in range(n):
        if i < 2 or i >= n - 2:
            filtered.append(intensities[i])
        else:
            avg = sum(intensities[i-2:i+3]) / 5.0
            filtered.append(avg)

    peaks = []
    for i in range(1, n - 1):
        if filtered[i] > filtered[i-1] and filtered[i] > filtered[i+1]:
            peaks.append((wavelengths[i], filtered[i]))

    max_intensity = max(filtered) if filtered else 1.0

    plot = []
    for i in range(n):
        stars = math.floor((filtered[i] / max_intensity) * 20)
        if stars < 0:
            stars = 0
        plot.append((wavelengths[i], stars))

    return wavelengths, filtered, peaks, plot

def test_c_and_bash_files_exist():
    assert os.path.isfile("/home/user/filter.c"), "Missing /home/user/filter.c"
    assert os.path.isfile("/home/user/filter.bin"), "Missing /home/user/filter.bin"
    assert os.path.isfile("/home/user/process_spectra.sh"), "Missing /home/user/process_spectra.sh"
    assert os.access("/home/user/process_spectra.sh", os.X_OK), "/home/user/process_spectra.sh is not executable"

def test_filtered_spectra():
    assert os.path.isfile(FILTERED_FILE), f"Missing {FILTERED_FILE}"
    wavelengths, filtered, _, _ = get_expected_data()

    with open(FILTERED_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == len(wavelengths), f"Expected {len(wavelengths)} lines in {FILTERED_FILE}, got {len(lines)}"

    for i, line in enumerate(lines):
        parts = line.split()
        assert len(parts) == 2, f"Line {i+1} in {FILTERED_FILE} is malformed: {line}"
        w = int(parts[0])
        fi = float(parts[1])

        expected_w = wavelengths[i]
        expected_fi = f"{filtered[i]:.2f}"

        assert w == expected_w, f"Line {i+1} wavelength mismatch: expected {expected_w}, got {w}"
        assert f"{fi:.2f}" == expected_fi, f"Line {i+1} intensity mismatch: expected {expected_fi}, got {fi:.2f}"

def test_peaks_log():
    assert os.path.isfile(PEAKS_FILE), f"Missing {PEAKS_FILE}"
    _, _, peaks, _ = get_expected_data()

    with open(PEAKS_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    # Filter out empty lines
    lines = [l for l in lines if l.strip()]

    assert len(lines) == len(peaks), f"Expected {len(peaks)} peaks in {PEAKS_FILE}, got {len(lines)}"

    for i, line in enumerate(lines):
        parts = line.split()
        assert len(parts) == 2, f"Peak line {i+1} is malformed: {line}"
        w = int(parts[0])
        fi = float(parts[1])

        expected_w = peaks[i][0]
        expected_fi = f"{peaks[i][1]:.2f}"

        assert w == expected_w, f"Peak {i+1} wavelength mismatch: expected {expected_w}, got {w}"
        assert f"{fi:.2f}" == expected_fi, f"Peak {i+1} intensity mismatch: expected {expected_fi}, got {fi:.2f}"

def test_plot_txt():
    assert os.path.isfile(PLOT_FILE), f"Missing {PLOT_FILE}"
    _, _, _, plot = get_expected_data()

    with open(PLOT_FILE, "r") as f:
        lines = f.read().strip().split('\n')

    # Filter out empty lines
    lines = [l for l in lines if l.strip()]

    assert len(lines) == len(plot), f"Expected {len(plot)} lines in {PLOT_FILE}, got {len(lines)}"

    for i, line in enumerate(lines):
        expected_w = plot[i][0]
        expected_stars = plot[i][1]

        expected_prefix = f"{expected_w} | "
        assert line.startswith(expected_prefix), f"Line {i+1} in {PLOT_FILE} should start with '{expected_prefix}'"

        stars_part = line[len(expected_prefix):]
        assert stars_part == "*" * expected_stars, f"Line {i+1} in {PLOT_FILE} should have {expected_stars} stars, got {len(stars_part)}: '{stars_part}'"