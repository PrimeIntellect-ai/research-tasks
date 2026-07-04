# test_final_state.py
import os
import csv
import pytest

def parse_fasta(filepath):
    sequences = {}
    with open(filepath, 'r') as f:
        seq_id = None
        seq_data = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if seq_id is not None:
                    sequences[seq_id] = "".join(seq_data)
                seq_id = line[1:]
                seq_data = []
            else:
                seq_data.append(line)
        if seq_id is not None:
            sequences[seq_id] = "".join(seq_data)
    return sequences

def parse_signals(filepath):
    signals = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            seq_id = row['SeqID']
            wn = int(row['wavenumber'])
            intensity = float(row['intensity'])
            if seq_id not in signals:
                signals[seq_id] = []
            signals[seq_id].append((wn, intensity))
    for seq_id in signals:
        signals[seq_id].sort(key=lambda x: x[0])
    return signals

def compute_expected_data():
    fasta_path = "/home/user/data/sequences.fasta"
    signals_path = "/home/user/data/signals.csv"

    if not os.path.exists(fasta_path) or not os.path.exists(signals_path):
        pytest.skip("Input files missing, cannot compute expected data.")

    sequences = parse_fasta(fasta_path)
    signals = parse_signals(signals_path)

    motif = "CGTAGCTACG"
    expected_rows = []

    for seq_id in sorted(sequences.keys()):
        seq = sequences[seq_id]
        primer_idx = seq.find(motif)
        if primer_idx == -1:
            continue

        if seq_id not in signals:
            continue

        signal_data = signals[seq_id]
        wavenumbers = [x[0] for x in signal_data]
        intensities = [x[1] for x in signal_data]

        # Trapezoidal rule
        area = 0.0
        for i in range(len(wavenumbers) - 1):
            dx = wavenumbers[i+1] - wavenumbers[i]
            y_avg = (intensities[i] + intensities[i+1]) / 2.0
            area += dx * y_avg

        # Second derivative and sharp peaks
        sharp_peaks = 0
        for i in range(1, len(intensities) - 1):
            sec_deriv = intensities[i-1] - 2 * intensities[i] + intensities[i+1]
            if sec_deriv < -1.5:
                sharp_peaks += 1

        expected_rows.append({
            "SeqID": seq_id,
            "PrimerIndex": str(primer_idx),
            "TotalArea": f"{round(area, 1):.1f}",
            "SharpPeakCount": str(sharp_peaks)
        })

    return expected_rows

def test_output_file_exists():
    output_path = "/home/user/output/training_data.csv"
    assert os.path.exists(output_path), f"Expected output file not found at {output_path}"

def test_output_file_content():
    output_path = "/home/user/output/training_data.csv"
    assert os.path.exists(output_path), f"Expected output file not found at {output_path}"

    expected_rows = compute_expected_data()

    with open(output_path, 'r') as f:
        reader = csv.DictReader(f)
        actual_headers = reader.fieldnames
        actual_rows = list(reader)

    expected_headers = ["SeqID", "PrimerIndex", "TotalArea", "SharpPeakCount"]
    assert actual_headers == expected_headers, f"Headers mismatch. Expected {expected_headers}, got {actual_headers}"

    assert len(actual_rows) == len(expected_rows), f"Row count mismatch. Expected {len(expected_rows)} rows, got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual["SeqID"] == expected["SeqID"], f"Row {i+1}: SeqID mismatch. Expected {expected['SeqID']}, got {actual['SeqID']}"
        assert actual["PrimerIndex"] == expected["PrimerIndex"], f"Row {i+1}: PrimerIndex mismatch for {expected['SeqID']}. Expected {expected['PrimerIndex']}, got {actual['PrimerIndex']}"

        # Allow some float formatting flexibility
        actual_area = float(actual["TotalArea"])
        expected_area = float(expected["TotalArea"])
        assert abs(actual_area - expected_area) < 0.05, f"Row {i+1}: TotalArea mismatch for {expected['SeqID']}. Expected {expected_area}, got {actual_area}"

        assert actual["SharpPeakCount"] == expected["SharpPeakCount"], f"Row {i+1}: SharpPeakCount mismatch for {expected['SeqID']}. Expected {expected['SharpPeakCount']}, got {actual['SharpPeakCount']}"