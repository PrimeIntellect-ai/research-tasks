# test_final_state.py
import os
import csv
import math

def compute_mean(arr):
    return sum(arr) / len(arr)

def compute_std(arr, mean_val, ddof=0):
    variance = sum((x - mean_val) ** 2 for x in arr) / (len(arr) - ddof)
    return math.sqrt(variance)

def compute_corr(x, y, mean_x, mean_y, std_x, std_y):
    if std_x == 0 or std_y == 0:
        return 0.0
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
    return cov / (std_x * std_y)

def test_joined_csv_exists_and_correct():
    joined_path = "/home/user/data/joined.csv"
    assert os.path.isfile(joined_path), f"File {joined_path} does not exist."

    # Read original files
    features = {}
    with open("/home/user/data/features.csv", "r") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            features[int(row[0])] = [float(x) for x in row[1:4]]

    targets = {}
    with open("/home/user/data/targets.csv", "r") as f:
        reader = csv.reader(f)
        next(reader) # skip header
        for row in reader:
            targets[int(row[0])] = float(row[1])

    # Inner join and sort
    common_ids = sorted(list(set(features.keys()).intersection(set(targets.keys()))))
    expected_rows = []
    for cid in common_ids:
        expected_rows.append([cid] + features[cid] + [targets[cid]])

    # Read joined.csv
    actual_rows = []
    with open(joined_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append([float(x) for x in row])

    assert len(actual_rows) == len(expected_rows), "joined.csv does not have the correct number of rows."

    for act, exp in zip(actual_rows, expected_rows):
        assert act[0] == exp[0], "joined.csv is not sorted by id or has incorrect ids."
        for a, e in zip(act, exp):
            assert math.isclose(a, e, rel_tol=1e-5, abs_tol=1e-5), "joined.csv values do not match expected inner join."

def test_pipeline_cpp_exists():
    assert os.path.isfile("/home/user/pipeline.cpp"), "File /home/user/pipeline.cpp does not exist."

def test_final_mse_correct():
    mse_path = "/home/user/final_mse.txt"
    assert os.path.isfile(mse_path), f"File {mse_path} does not exist."

    # Compute expected MSE
    features = {}
    with open("/home/user/data/features.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            features[int(row[0])] = [float(x) for x in row[1:4]]

    targets = {}
    with open("/home/user/data/targets.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            targets[int(row[0])] = float(row[1])

    common_ids = sorted(list(set(features.keys()).intersection(set(targets.keys()))))
    dataset = []
    for cid in common_ids:
        dataset.append(features[cid] + [targets[cid]])

    n = len(dataset)
    fold_size = n // 5
    mses_pop = []
    mses_samp = []

    for i in range(5):
        val_idx = set(range(i * fold_size, (i + 1) * fold_size))
        train_idx = [idx for idx in range(n) if idx not in val_idx]
        val_idx = sorted(list(val_idx))

        train_f1 = [dataset[idx][0] for idx in train_idx]
        train_f2 = [dataset[idx][1] for idx in train_idx]
        train_f3 = [dataset[idx][2] for idx in train_idx]
        train_t = [dataset[idx][3] for idx in train_idx]

        val_f1 = [dataset[idx][0] for idx in val_idx]
        val_f2 = [dataset[idx][1] for idx in val_idx]
        val_f3 = [dataset[idx][2] for idx in val_idx]
        val_t = [dataset[idx][3] for idx in val_idx]

        # Means
        m1 = compute_mean(train_f1)
        m2 = compute_mean(train_f2)
        m3 = compute_mean(train_f3)
        mt = compute_mean(train_t)

        # Stds (population)
        s1_p = compute_std(train_f1, m1, ddof=0)
        s2_p = compute_std(train_f2, m2, ddof=0)
        s3_p = compute_std(train_f3, m3, ddof=0)
        st_p = compute_std(train_t, mt, ddof=0)

        # Stds (sample)
        s1_s = compute_std(train_f1, m1, ddof=1)
        s2_s = compute_std(train_f2, m2, ddof=1)
        s3_s = compute_std(train_f3, m3, ddof=1)
        st_s = compute_std(train_t, mt, ddof=1)

        def compute_fold_mse(s1, s2, s3, st):
            # Normalize train
            tn1 = [(x - m1) / s1 for x in train_f1]
            tn2 = [(x - m2) / s2 for x in train_f2]
            tn3 = [(x - m3) / s3 for x in train_f3]

            # Normalize val
            vn1 = [(x - m1) / s1 for x in val_f1]
            vn2 = [(x - m2) / s2 for x in val_f2]
            vn3 = [(x - m3) / s3 for x in val_f3]

            c1 = compute_corr(tn1, train_t, compute_mean(tn1), mt, compute_std(tn1, compute_mean(tn1), ddof=0), st)
            c2 = compute_corr(tn2, train_t, compute_mean(tn2), mt, compute_std(tn2, compute_mean(tn2), ddof=0), st)
            c3 = compute_corr(tn3, train_t, compute_mean(tn3), mt, compute_std(tn3, compute_mean(tn3), ddof=0), st)

            fold_mse = 0
            for j in range(len(val_idx)):
                pred = c1 * vn1[j] + c2 * vn2[j] + c3 * vn3[j]
                fold_mse += (pred - val_t[j]) ** 2
            return fold_mse / len(val_idx)

        mses_pop.append(compute_fold_mse(s1_p, s2_p, s3_p, st_p))
        mses_samp.append(compute_fold_mse(s1_s, s2_s, s3_s, st_s))

    avg_mse_pop = sum(mses_pop) / 5
    avg_mse_samp = sum(mses_samp) / 5

    with open(mse_path, "r") as f:
        actual_mse_str = f.read().strip()

    try:
        actual_mse = float(actual_mse_str)
    except ValueError:
        assert False, f"Could not parse final_mse.txt as a float. Got: {actual_mse_str}"

    # Allow for either population or sample std formulation, plus a tolerance
    is_pop_close = math.isclose(actual_mse, avg_mse_pop, abs_tol=0.1)
    is_samp_close = math.isclose(actual_mse, avg_mse_samp, abs_tol=0.1)

    assert is_pop_close or is_samp_close, f"Expected MSE around {avg_mse_pop:.4f} or {avg_mse_samp:.4f}, but got {actual_mse:.4f}."