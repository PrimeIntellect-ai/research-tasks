# test_final_state.py

import os
import random
import subprocess
import pytest

def test_go_cleaner_exists():
    """Test that the compiled Go cleaner exists and is executable."""
    go_cleaner_path = "/home/user/go_cleaner"
    assert os.path.exists(go_cleaner_path), f"Go cleaner missing at {go_cleaner_path}"
    assert os.path.isfile(go_cleaner_path), f"{go_cleaner_path} is not a file"
    assert os.access(go_cleaner_path, os.X_OK), f"{go_cleaner_path} is not executable"

def test_fuzz_equivalence():
    """Fuzz test the Go cleaner against the legacy cleaner."""
    legacy_cleaner = "/app/legacy_cleaner"
    go_cleaner = "/home/user/go_cleaner"

    random.seed(42)

    for i in range(100):
        num_floats = random.randint(1, 100)
        floats = [random.uniform(-10000.0, 10000.0) for _ in range(num_floats)]
        input_str = " ".join(f"{f:.6f}" for f in floats) + "\n"

        # Run legacy cleaner
        legacy_proc = subprocess.run(
            [legacy_cleaner],
            input=input_str,
            text=True,
            capture_output=True,
            check=True
        )
        legacy_output = legacy_proc.stdout.strip()

        # Run go cleaner
        go_proc = subprocess.run(
            [go_cleaner],
            input=input_str,
            text=True,
            capture_output=True,
            check=True
        )
        go_output = go_proc.stdout.strip()

        assert go_output == legacy_output, (
            f"Output mismatch on iteration {i}.\n"
            f"Input: {input_str[:100]}...\n"
            f"Legacy output: {legacy_output[:100]}...\n"
            f"Go output: {go_output[:100]}...\n"
        )

def test_setup_db_script():
    """Test that the setup_db script exists, runs, and creates the correct DB schema."""
    script_path = "/home/user/setup_db.sh"
    assert os.path.exists(script_path), f"Database setup script missing at {script_path}"

    # Run the script
    subprocess.run(["bash", script_path], check=True)

    # Check if database exists
    db_check = subprocess.run(
        ["psql", "-U", "postgres", "-tAc", "SELECT 1 FROM pg_database WHERE datname='sensor_data'"],
        capture_output=True, text=True
    )
    assert db_check.stdout.strip() == "1", "Database 'sensor_data' does not exist."

    # Check if table exists with correct columns
    table_check = subprocess.run(
        ["psql", "-U", "postgres", "-d", "sensor_data", "-tAc", 
         "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='cleaned_features' ORDER BY column_name"],
        capture_output=True, text=True
    )

    columns = table_check.stdout.strip().split("\n")
    assert len(columns) == 2, f"Expected 2 columns in cleaned_features, got {len(columns)}"

    col_dict = {}
    for col in columns:
        parts = col.split("|")
        if len(parts) == 2:
            col_dict[parts[0]] = parts[1]

    assert "id" in col_dict, "Column 'id' missing"
    assert "value" in col_dict, "Column 'value' missing"

    assert col_dict["id"] == "integer", f"Expected 'id' to be integer, got {col_dict['id']}"
    assert col_dict["value"] == "double precision", f"Expected 'value' to be double precision, got {col_dict['value']}"