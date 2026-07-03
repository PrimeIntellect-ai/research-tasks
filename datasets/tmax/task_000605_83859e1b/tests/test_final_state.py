# test_final_state.py
import os
import csv

def parse_fasta(filepath):
    sequences = []
    with open(filepath, 'r') as f:
        current_id = None
        current_seq = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_id is not None:
                    sequences.append((current_id, "".join(current_seq)))
                current_id = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
        if current_id is not None:
            sequences.append((current_id, "".join(current_seq)))
    return sequences

def sequence_to_signal(seq):
    mapping = {'A': 1.5, 'C': 0.5, 'G': -0.5, 'T': -1.5}
    return [mapping.get(char.upper(), 0.0) for char in seq]

def calculate_integrals(signal):
    n = len(signal)
    if n < 2:
        return 0.0, 0.0

    # Calculate I
    I = sum((signal[i] + signal[i+1]) / 2.0 for i in range(n - 1))

    # Calculate D
    D = [signal[i+1] - signal[i] for i in range(n - 1)]

    # Calculate DI
    if len(D) < 2:
        DI = 0.0
    else:
        DI = sum((abs(D[i]) + abs(D[i+1])) / 2.0 for i in range(len(D) - 1))

    return I, DI

def test_results_csv_exists():
    csv_path = "/home/user/results.csv"
    assert os.path.isfile(csv_path), f"The output CSV file {csv_path} does not exist."

def test_results_csv_content():
    fasta_path = "/home/user/sequences.fasta"
    csv_path = "/home/user/results.csv"

    assert os.path.isfile(fasta_path), f"Input FASTA file {fasta_path} is missing."
    assert os.path.isfile(csv_path), f"Output CSV file {csv_path} is missing."

    sequences = parse_fasta(fasta_path)
    expected_results = []
    for seq_id, seq in sequences:
        signal = sequence_to_signal(seq)
        I, DI = calculate_integrals(signal)
        expected_results.append({
            'ID': seq_id,
            'I': f"{I:.2f}",
            'DI': f"{DI:.2f}"
        })

    actual_results = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['ID', 'I', 'DI'], f"CSV header is incorrect. Expected ['ID', 'I', 'DI'], got {reader.fieldnames}"
        for row in reader:
            actual_results.append(row)

    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} rows in CSV, but found {len(actual_results)}."

    for i, (expected, actual) in enumerate(zip(expected_results, actual_results)):
        assert actual['ID'] == expected['ID'], f"Row {i+1}: Expected ID '{expected['ID']}', got '{actual['ID']}'."
        assert actual['I'] == expected['I'], f"Row {i+1} ({expected['ID']}): Expected I={expected['I']}, got I={actual['I']}."
        assert actual['DI'] == expected['DI'], f"Row {i+1} ({expected['ID']}): Expected DI={expected['DI']}, got DI={actual['DI']}."