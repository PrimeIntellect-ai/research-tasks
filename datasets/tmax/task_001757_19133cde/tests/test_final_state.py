# test_final_state.py

import os

def test_clean_stats_exists():
    """
    Check if the clean_stats.txt file was generated.
    """
    file_path = "/home/user/clean_stats.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing. Did the C program run and generate it?"

def test_clean_stats_content():
    """
    Verify the contents of clean_stats.txt by recomputing the expected 
    values from the actual sensor_data.csv file.
    """
    data_path = "/home/user/sensor_data.csv"
    stats_path = "/home/user/clean_stats.txt"

    assert os.path.isfile(data_path), f"The file {data_path} is missing."
    assert os.path.isfile(stats_path), f"The file {stats_path} is missing."

    valid_x = []
    valid_y = []

    # Read and filter data based on requirements
    with open(data_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 2:
                x, y = float(parts[0]), float(parts[1])
                # Filter out corrupted rows
                if -50.0 <= x <= 50.0 and -50.0 <= y <= 50.0:
                    valid_x.append(x)
                    valid_y.append(y)

    n = len(valid_x)
    assert n > 1, "Not enough valid data points to compute statistics."

    # Compute statistics
    mean_x = sum(valid_x) / n
    mean_y = sum(valid_y) / n

    cov_xx = sum((x - mean_x)**2 for x in valid_x) / (n - 1)
    cov_yy = sum((y - mean_y)**2 for y in valid_y) / (n - 1)
    cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(valid_x, valid_y)) / (n - 1)

    m = cov_xy / cov_xx
    c = mean_y - m * mean_x

    # Format expected output
    expected_lines = [
        f"Valid Count: {n}",
        f"Mean X: {mean_x:.4f}",
        f"Mean Y: {mean_y:.4f}",
        f"Cov(X,X): {cov_xx:.4f}",
        f"Cov(Y,Y): {cov_yy:.4f}",
        f"Cov(X,Y): {cov_xy:.4f}",
        f"Slope (m): {m:.4f}",
        f"Intercept (c): {c:.4f}"
    ]
    expected_content = "\n".join(expected_lines)

    # Read actual output
    with open(stats_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {stats_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{actual_content}"
    )