# test_final_state.py
import os
import subprocess
import tempfile

def test_pipeline_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"Script not found at {path}"
    assert os.access(path, os.X_OK), f"Script {path} is not executable"

def test_pipeline_output():
    path = "/home/user/pipeline.sh"
    dataset = "/home/user/dataset.csv"
    rand_src = "/home/user/fixed_rand"

    assert os.path.isfile(dataset), f"Dataset is missing: {dataset}"
    assert os.path.isfile(rand_src), f"Random source is missing: {rand_src}"

    # Recompute the expected value exactly as the bash logic would
    with open(dataset, 'r') as f:
        lines = f.read().strip().split('\n')

    # Exclude header
    data = lines[1:]
    N = len(data)
    train_n = N * 70 // 100
    test_n = N - train_n

    train_init = data[:train_n]
    test_set = data[train_n:]

    # Use shuf to get the exact bootstrapped sample
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.write('\n'.join(train_init) + '\n')
        temp_train_path = f.name

    try:
        cmd_shuf = ['shuf', f'--random-source={rand_src}', '-r', '-n', str(train_n), temp_train_path]
        res_shuf = subprocess.run(cmd_shuf, capture_output=True, text=True, check=True)
        train_boot = [row for row in res_shuf.stdout.strip().split('\n') if row]
    finally:
        os.remove(temp_train_path)

    # Calculate means from bootstrapped training set
    sum_x = 0.0
    sum_y = 0.0
    for row in train_boot:
        parts = row.split(',')
        sum_x += float(parts[1])
        sum_y += float(parts[2])

    mean_x = sum_x / train_n
    mean_y = sum_y / train_n

    # Calculate sample covariance on test set using training means
    sum_prod = 0.0
    for row in test_set:
        if not row:
            continue
        parts = row.split(',')
        cx = float(parts[1]) - mean_x
        cy = float(parts[2]) - mean_y
        sum_prod += cx * cy

    expected_cov = sum_prod / (test_n - 1)
    expected_str = f"{expected_cov:.4f}"

    # Run student script
    cmd = [path, dataset, rand_src]
    res = subprocess.run(cmd, capture_output=True, text=True)

    assert res.returncode == 0, f"Script failed with exit code {res.returncode}. Stderr: {res.stderr}"

    output = res.stdout.strip()
    assert output == expected_str, f"Expected covariance '{expected_str}', but got '{output}'"