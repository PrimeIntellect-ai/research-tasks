# test_final_state.py
import os
import json
import csv
import stat

def test_run_etl_sh():
    script_path = "/home/user/run_etl.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "OMP_NUM_THREADS=1" in content, "OMP_NUM_THREADS=1 not found in run_etl.sh"
    assert "OPENBLAS_NUM_THREADS=1" in content, "OPENBLAS_NUM_THREADS=1 not found in run_etl.sh"
    assert "MKL_NUM_THREADS=1" in content, "MKL_NUM_THREADS=1 not found in run_etl.sh"

def test_best_params_json():
    json_path = "/home/user/best_params.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    expected_keys = {"alpha_1", "alpha_2", "lambda_1", "lambda_2"}
    assert set(params.keys()) == expected_keys, f"Expected keys {expected_keys} in best_params.json, found {set(params.keys())}"

def test_imputed_sensor_data():
    orig_path = "/home/user/sensor_data.csv"
    imputed_path = "/home/user/imputed_sensor_data.csv"

    assert os.path.exists(imputed_path), f"File {imputed_path} does not exist."

    with open(orig_path, "r") as f_orig, open(imputed_path, "r") as f_imp:
        reader_orig = csv.DictReader(f_orig)
        reader_imp = csv.DictReader(f_imp)

        expected_columns = ["id", "sensor_A", "sensor_B", "sensor_C", "sensor_C_std"]
        assert reader_imp.fieldnames == expected_columns, f"Expected columns {expected_columns}, got {reader_imp.fieldnames}"

        orig_rows = list(reader_orig)
        imp_rows = list(reader_imp)

        assert len(orig_rows) == len(imp_rows), "Number of rows in imputed data does not match original data."

        for i, (r_orig, r_imp) in enumerate(zip(orig_rows, imp_rows)):
            assert r_orig["id"] == r_imp["id"], f"Row {i}: ID mismatch"
            assert r_orig["sensor_A"] == r_imp["sensor_A"], f"Row {i}: sensor_A mismatch"
            assert r_orig["sensor_B"] == r_imp["sensor_B"], f"Row {i}: sensor_B mismatch"

            c_std = float(r_imp["sensor_C_std"])

            if r_orig["sensor_C"] == "":
                # Was missing, should be imputed
                assert r_imp["sensor_C"] != "", f"Row {i}: sensor_C was not imputed"
                assert c_std > 0.0, f"Row {i}: sensor_C_std should be > 0.0 for imputed values, got {c_std}"
            else:
                # Was not missing, should match original and std should be 0.0
                # Using float comparison to handle formatting differences
                assert abs(float(r_orig["sensor_C"]) - float(r_imp["sensor_C"])) < 1e-6, f"Row {i}: sensor_C was changed but originally not missing"
                assert c_std == 0.0, f"Row {i}: sensor_C_std should be 0.0 for existing values, got {c_std}"