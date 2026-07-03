# test_final_state.py
import os

def test_processed_embeddings():
    raw_data_path = '/home/user/raw_data.csv'
    output_path = '/home/user/processed_embeddings.csv'

    assert os.path.isfile(raw_data_path), f"Raw data file {raw_data_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    expected_lines = []
    with open(raw_data_path, 'r') as infile:
        for L, line in enumerate(infile):
            if (L * 9973) % 100000 < 1000:
                x = [float(val) for val in line.strip().split(',')]
                e0, e1, e2 = 0.0, 0.0, 0.0
                for j in range(10):
                    weight = j + 1
                    e0 += x[j] * weight
                    e1 += x[j] * (weight ** 2)
                    e2 += x[j] * (weight ** 3)
                expected_lines.append(f"{e0:.4f},{e1:.4f},{e2:.4f}\n")

    with open(output_path, 'r') as outfile:
        actual_lines = outfile.readlines()

    assert len(actual_lines) == len(expected_lines), \
        f"Expected {len(expected_lines)} lines in {output_path}, but found {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual.strip() == expected.strip(), \
            f"Mismatch at line {i+1} in {output_path}.\nExpected: {expected.strip()}\nActual: {actual.strip()}"

def test_cpp_code_exists():
    cpp_path = '/home/user/prepare.cpp'
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."