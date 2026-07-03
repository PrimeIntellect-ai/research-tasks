# test_final_state.py
import os
import csv
import math
import subprocess
import sys

def test_pca_result_exists_and_format():
    path = "/home/user/pca_result.csv"
    assert os.path.exists(path), f"Missing file: {path}"

    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['id', 'pc1', 'pc2'], f"Incorrect columns. Expected ['id', 'pc1', 'pc2'], got {header}"

        rows = list(reader)
        assert len(rows) > 0, "The result CSV is empty except for the header"

        for i, row in enumerate(rows):
            id_val = row[0]
            assert '.' not in id_val, f"Row {i+1}: 'id' column contains float formatting ('{id_val}') instead of integer."
            try:
                int(id_val)
            except ValueError:
                assert False, f"Row {i+1}: 'id' column value '{id_val}' is not a valid integer."

def test_pca_result_values():
    # Since we cannot import pandas/sklearn directly in the test (stdlib only),
    # we use a subprocess to generate the expected results using the environment's libraries.
    script = """
import pandas as pd
from sklearn.decomposition import PCA

df_a = pd.read_csv('/home/user/data/dataset_A.csv')
df_b = pd.read_csv('/home/user/data/dataset_B.csv')

df = pd.merge(df_a, df_b, on='id', how='outer')
df = df.sort_values('id', ascending=True)

features = ['f1', 'f2', 'f3', 'f4', 'f5']
df[features] = df[features].fillna(0)

pca = PCA(n_components=2, svd_solver='full', random_state=42)
pca_features = pca.fit_transform(df[features])

result = pd.DataFrame({
    'id': df['id'].astype(int),
    'pc1': pca_features[:, 0],
    'pc2': pca_features[:, 1]
})
result.to_csv('/tmp/expected_pca_result.csv', index=False)
"""
    script_path = "/tmp/generate_expected_pca.py"
    with open(script_path, "w") as f:
        f.write(script)

    subprocess.run([sys.executable, script_path], check=True)

    expected_path = "/tmp/expected_pca_result.csv"
    user_path = "/home/user/pca_result.csv"

    with open(expected_path, "r") as f_exp, open(user_path, "r") as f_usr:
        exp_reader = csv.reader(f_exp)
        usr_reader = csv.reader(f_usr)

        next(exp_reader) # skip header
        next(usr_reader) # skip header

        exp_rows = list(exp_reader)
        usr_rows = list(usr_reader)

    assert len(usr_rows) == len(exp_rows), f"Expected {len(exp_rows)} rows, but got {len(usr_rows)} rows."

    for i, (usr_row, exp_row) in enumerate(zip(usr_rows, exp_rows)):
        assert usr_row[0] == exp_row[0], f"Row {i+1}: Expected id {exp_row[0]}, got {usr_row[0]}"

        try:
            usr_pc1 = float(usr_row[1])
            usr_pc2 = float(usr_row[2])
        except ValueError:
            assert False, f"Row {i+1}: pc1 or pc2 is not a valid float."

        exp_pc1 = float(exp_row[1])
        exp_pc2 = float(exp_row[2])

        assert math.isclose(usr_pc1, exp_pc1, abs_tol=1e-4), f"Row {i+1} (id={usr_row[0]}): pc1 value mismatch. Expected {exp_pc1}, got {usr_pc1}"
        assert math.isclose(usr_pc2, exp_pc2, abs_tol=1e-4), f"Row {i+1} (id={usr_row[0]}): pc2 value mismatch. Expected {exp_pc2}, got {usr_pc2}"