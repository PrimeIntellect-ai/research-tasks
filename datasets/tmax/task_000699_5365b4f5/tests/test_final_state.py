# test_final_state.py
import os
import csv

def test_test_result_txt():
    path = "/home/user/test_result.txt"
    assert os.path.exists(path), f"File {path} is missing. The test script must create it."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "REPRODUCIBILITY_PASSED", f"Expected 'REPRODUCIBILITY_PASSED' in {path}, got '{content}'"

def test_features_csv_format():
    path = "/home/user/features.csv"
    assert os.path.exists(path), f"File {path} is missing. The pipeline should have generated it."

    expected_category_ids = ["1", "2", "3", "-1", "-1"]
    actual_category_ids = []

    with open(path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "features.csv is empty."
        assert "category_id" in header, "features.csv is missing 'category_id' column."

        cat_idx = header.index("category_id")
        for row in reader:
            if len(row) > cat_idx:
                actual_category_ids.append(row[cat_idx])

    assert actual_category_ids == expected_category_ids, (
        f"Expected category_id values to be {expected_category_ids}, "
        f"but got {actual_category_ids}. Make sure they are integers and not floats (e.g. no '.0')."
    )

def test_test_pipeline_script_exists():
    path = "/home/user/test_pipeline.py"
    assert os.path.exists(path), f"File {path} is missing. You need to create the test script."