# test_final_state.py

import os
import struct

def test_integral_result_file_exists():
    path = "/home/user/integral_result.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the Rust project and save the output?"

def test_integral_result_value():
    data_path = "/home/user/bio_mcmc/sequence_likelihoods.txt"
    assert os.path.isfile(data_path), f"Data file {data_path} is missing."

    data = []
    with open(data_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) == 2:
                # Simulate f32 parsing to match Rust's f32 behavior
                x_f32 = struct.unpack('f', struct.pack('f', float(parts[0])))[0]
                y_f32 = struct.unpack('f', struct.pack('f', float(parts[1])))[0]
                data.append((x_f32, y_f32))

    data.sort(key=lambda item: item[0])

    expected_integral = 0.0
    for i in range(len(data) - 1):
        x1, y1 = data[i]
        x2, y2 = data[i+1]
        # Cast to f64 for accumulation (Python floats are f64)
        expected_integral += 0.5 * (float(y1) + float(y2)) * (float(x2) - float(x1))

    expected_str = f"{expected_integral:.4f}"

    result_path = "/home/user/integral_result.txt"
    with open(result_path, 'r') as f:
        actual_str = f.read().strip()

    # Extract the number if they included "Integral: " prefix
    if "Integral:" in actual_str:
        actual_str = actual_str.split("Integral:")[1].strip()

    assert actual_str == expected_str, f"Expected integral result to be {expected_str}, but got {actual_str}"

def test_rust_code_modifications():
    main_rs_path = "/home/user/bio_mcmc/src/main.rs"
    assert os.path.isfile(main_rs_path), f"File {main_rs_path} is missing."

    with open(main_rs_path, 'r') as f:
        content = f.read()

    assert "f64" in content, "The Rust code does not appear to use f64 for the accumulation as requested."
    assert "into_par_iter" not in content, "The Rust code still seems to use unordered parallel iteration (`into_par_iter`). It should be sequential."