# test_final_state.py
import os
import csv
import json
import math

def test_processed_feedback_csv():
    file_path = '/home/user/processed_feedback.csv'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        assert fieldnames is not None, f"{file_path} is empty or invalid."
        assert 'id' in fieldnames, "Column 'id' missing in processed_feedback.csv."
        assert 'category' in fieldnames, "Column 'category' missing in processed_feedback.csv."
        assert 'text' in fieldnames, "Column 'text' missing in processed_feedback.csv."
        assert 'sim_to_product' in fieldnames, "Column 'sim_to_product' missing in processed_feedback.csv."

        rows = list(reader)
        assert len(rows) == 100, f"Expected 100 rows in {file_path}, found {len(rows)}."

        for row in rows:
            try:
                sim = float(row['sim_to_product'])
            except ValueError:
                assert False, f"sim_to_product value '{row['sim_to_product']}' for id {row['id']} is not a valid float."

            # Check 4 decimal places roughly (or exactly)
            parts = row['sim_to_product'].split('.')
            if len(parts) == 2:
                assert len(parts[1]) <= 4, f"sim_to_product value '{row['sim_to_product']}' is not rounded to 4 decimal places."

def test_top_5_support_txt():
    file_path = '/home/user/top_5_support.txt'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 IDs in {file_path}, found {len(lines)}."
    for line in lines:
        assert line.startswith("ID_"), f"Expected ID format 'ID_xxx', found '{line}'."

def test_stat_results_json():
    file_path = '/home/user/stat_results.json'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} is not valid JSON."

    expected_keys = {"t_statistic", "p_value", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"Expected keys {expected_keys} in {file_path}, found {set(data.keys())}."

    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"Value for {key} must be a number."

        # Check rounding to 4 decimal places
        val_str = str(data[key])
        if '.' in val_str:
            decimals = len(val_str.split('.')[1])
            assert decimals <= 4, f"Value for {key} ({data[key]}) is not rounded to 4 decimal places."

def test_internal_consistency():
    # Verify that the top 5 support IDs actually correspond to the highest sim_to_product in the CSV
    csv_path = '/home/user/processed_feedback.csv'
    txt_path = '/home/user/top_5_support.txt'

    if not os.path.exists(csv_path) or not os.path.exists(txt_path):
        return # Handled by previous tests

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        support_rows = [row for row in reader if row.get('category') == 'Support']

    # Sort support rows by sim_to_product descending
    try:
        support_rows.sort(key=lambda x: float(x['sim_to_product']), reverse=True)
    except (ValueError, KeyError):
        return # Handled by previous tests

    expected_top_5_ids = [row['id'] for row in support_rows[:5]]

    with open(txt_path, 'r', encoding='utf-8') as f:
        actual_top_5_ids = [line.strip() for line in f if line.strip()]

    assert actual_top_5_ids == expected_top_5_ids, f"Top 5 IDs in {txt_path} do not match the highest sim_to_product Support rows in {csv_path}."

def test_stat_computation_consistency():
    # Verify that the t-test results match the data in the CSV
    csv_path = '/home/user/processed_feedback.csv'
    json_path = '/home/user/stat_results.json'

    if not os.path.exists(csv_path) or not os.path.exists(json_path):
        return

    prod_sims = []
    supp_sims = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                val = float(row['sim_to_product'])
                if row['category'] == 'Product':
                    prod_sims.append(val)
                elif row['category'] == 'Support':
                    supp_sims.append(val)
            except (ValueError, KeyError):
                pass

    if not prod_sims or not supp_sims:
        return

    mean_prod = sum(prod_sims) / len(prod_sims)
    mean_supp = sum(supp_sims) / len(supp_sims)

    var_prod = sum((x - mean_prod) ** 2 for x in prod_sims) / (len(prod_sims) - 1)
    var_supp = sum((x - mean_supp) ** 2 for x in supp_sims) / (len(supp_sims) - 1)

    se_diff = math.sqrt(var_prod / len(prod_sims) + var_supp / len(supp_sims))
    t_stat = (mean_prod - mean_supp) / se_diff

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    actual_t_stat = data.get('t_statistic')
    if actual_t_stat is not None:
        assert math.isclose(abs(actual_t_stat), abs(t_stat), rel_tol=1e-2), f"Calculated t-statistic {t_stat:.4f} does not match json file {actual_t_stat}."