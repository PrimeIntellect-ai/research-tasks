# test_final_state.py

import os
import csv
import stat

def test_run_sh_exists_and_executable():
    """Test that run.sh exists and is executable."""
    run_sh_path = "/home/user/run.sh"
    assert os.path.isfile(run_sh_path), f"File not found: {run_sh_path}. The run script is missing."

    st = os.stat(run_sh_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {run_sh_path} is not executable."

def test_run_sh_contents():
    """Test that run.sh sets the correct environment variables."""
    run_sh_path = "/home/user/run.sh"
    with open(run_sh_path, 'r') as f:
        content = f.read()

    assert "OMP_NUM_THREADS=1" in content, "run.sh is missing OMP_NUM_THREADS=1"
    assert "OPENBLAS_NUM_THREADS=1" in content, "run.sh is missing OPENBLAS_NUM_THREADS=1"
    assert "MKL_NUM_THREADS=1" in content, "run.sh is missing MKL_NUM_THREADS=1"

def test_recommendations_csv_structure():
    """Test that recommendations.csv exists and has the correct structure."""
    recommendations_path = "/home/user/recommendations.csv"
    assert os.path.isfile(recommendations_path), f"File not found: {recommendations_path}. The output file is missing."

    with open(recommendations_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['user_id', 'recommended_item'], f"Incorrect header in recommendations.csv: {header}"

        rows = list(reader)
        assert len(rows) == 200, f"Expected 200 rows in recommendations.csv, found {len(rows)}"

        # Check that user_ids are correct (last 200 users: U0800 to U0999)
        expected_user_ids = [f'U{i:04d}' for i in range(800, 1000)]
        actual_user_ids = [row[0] for row in rows]
        assert actual_user_ids == expected_user_ids, "The user_id column does not match the expected test set users."

        # Check that recommended_item are from the valid set
        valid_items = {'ItemA', 'ItemB', 'ItemC', 'ItemD', 'ItemE'}
        for i, row in enumerate(rows):
            assert len(row) == 2, f"Row {i+1} does not have exactly 2 columns."
            assert row[1] in valid_items, f"Invalid recommended_item '{row[1]}' in row {i+1}."