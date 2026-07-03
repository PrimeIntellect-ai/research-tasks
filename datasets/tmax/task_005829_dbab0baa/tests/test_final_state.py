# test_final_state.py
import os
import csv
import tarfile
import math

def test_script_exists_and_executable():
    script_path = "/home/user/process_sensors.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_processed_sensors_archive():
    archive_path = "/home/user/clean_data_archive.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tarball."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # Check that it contains the expected files
        csv_files = [n for n in names if n.endswith(".csv")]
        assert len(csv_files) >= 2, "Archive does not contain the expected CSV files."

def get_cleaned_value(val_str):
    if val_str == "NA":
        return 0.0
    val = float(val_str)
    if val > 50.0:
        return 50.0
    if val < -50.0:
        return -50.0
    return val

def test_processed_sensors_data():
    raw_dir = "/home/user/raw_sensors"
    processed_dir = "/home/user/processed_sensors"
    assert os.path.isdir(processed_dir), f"{processed_dir} does not exist."

    for filename in os.listdir(raw_dir):
        if not filename.endswith(".csv"):
            continue
        raw_path = os.path.join(raw_dir, filename)
        proc_path = os.path.join(processed_dir, filename)
        assert os.path.exists(proc_path), f"Processed file {proc_path} is missing."

        with open(raw_path, 'r') as fr, open(proc_path, 'r') as fp:
            raw_reader = csv.DictReader(fr)
            proc_reader = csv.DictReader(fp)

            assert raw_reader.fieldnames == proc_reader.fieldnames, f"Headers mismatch in {filename}"

            for raw_row, proc_row in zip(raw_reader, proc_reader):
                assert raw_row['id'] == proc_row['id'], "ID mismatch in processed data."
                for f in ['f1', 'f2', 'f3']:
                    expected_val = get_cleaned_value(raw_row[f])
                    actual_val = float(proc_row[f])
                    assert math.isclose(expected_val, actual_val, rel_tol=1e-5), \
                        f"Value mismatch in {filename} for id {raw_row['id']}, feature {f}. Expected {expected_val}, got {actual_val}"

def test_all_predictions():
    preds_path = "/home/user/all_predictions.csv"
    weights_path = "/home/user/model_weights.txt"
    raw_dir = "/home/user/raw_sensors"

    assert os.path.exists(preds_path), f"{preds_path} does not exist."
    assert os.path.exists(weights_path), f"{weights_path} does not exist."

    with open(weights_path, 'r') as fw:
        w_str = fw.read().strip().split(',')
        w1, w2, w3 = float(w_str[0]), float(w_str[1]), float(w_str[2])

    expected_preds = {}
    for filename in os.listdir(raw_dir):
        if not filename.endswith(".csv"):
            continue
        raw_path = os.path.join(raw_dir, filename)
        with open(raw_path, 'r') as fr:
            reader = csv.DictReader(fr)
            for row in reader:
                id_val = int(row['id'])
                f1 = get_cleaned_value(row['f1'])
                f2 = get_cleaned_value(row['f2'])
                f3 = get_cleaned_value(row['f3'])
                pred = (w1 * f1) + (w2 * f2) + (w3 * f3)
                expected_preds[id_val] = pred

    actual_ids = []
    actual_preds = {}
    with open(preds_path, 'r') as fp:
        reader = csv.reader(fp)
        header = next(reader)
        assert header == ['id', 'prediction'], f"Incorrect header in {preds_path}: {header}"

        for row in reader:
            if not row:
                continue
            id_val = int(row[0])
            pred_val = float(row[1])
            actual_ids.append(id_val)
            actual_preds[id_val] = pred_val

    # Check sorting
    assert actual_ids == sorted(actual_ids), "Predictions are not sorted by id in ascending order."

    # Check values
    assert len(actual_preds) == len(expected_preds), "Mismatch in total number of predictions."
    for id_val, exp_pred in expected_preds.items():
        assert id_val in actual_preds, f"ID {id_val} missing in predictions."
        assert math.isclose(exp_pred, actual_preds[id_val], rel_tol=1e-4, abs_tol=1e-4), \
            f"Prediction mismatch for ID {id_val}. Expected {exp_pred}, got {actual_preds[id_val]}"

def test_prediction_sum():
    preds_path = "/home/user/all_predictions.csv"
    sum_path = "/home/user/prediction_sum.txt"

    assert os.path.exists(preds_path), f"{preds_path} does not exist."
    assert os.path.exists(sum_path), f"{sum_path} does not exist."

    total_sum = 0.0
    with open(preds_path, 'r') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            total_sum += float(row['prediction'])

    with open(sum_path, 'r') as fs:
        sum_str = fs.read().strip()

    # Check formatting (2 decimal places)
    assert "." in sum_str and len(sum_str.split(".")[1]) == 2, f"Sum {sum_str} is not formatted to 2 decimal places."

    actual_sum = float(sum_str)
    assert math.isclose(total_sum, actual_sum, rel_tol=1e-4, abs_tol=1e-4), \
        f"Prediction sum mismatch. Expected {total_sum:.2f}, got {actual_sum}"