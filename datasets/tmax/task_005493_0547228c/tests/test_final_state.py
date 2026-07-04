# test_final_state.py
import os
import csv

def test_project_exists():
    """Ensure the Rust project exists and uses rayon."""
    cargo_toml_path = "/home/user/circle_data_gen/Cargo.toml"
    assert os.path.exists(cargo_toml_path), f"Cargo project file {cargo_toml_path} does not exist."

    with open(cargo_toml_path, "r") as f:
        content = f.read()
        assert "rayon" in content, "rayon dependency not found in Cargo.toml."

def test_convergence_log():
    """Ensure convergence.log has the exact expected lines."""
    log_path = "/home/user/convergence.log"
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "N=10, Area=3.20000",
        "N=20, Area=3.16000",
        "N=40, Area=3.14000",
        "N=80, Area=3.14000"
    ]
    assert lines == expected, f"convergence.log contents do not match expected.\nExpected: {expected}\nGot: {lines}"

def test_training_data_csv():
    """Ensure training_data.csv has the correct header, row count, and valid labels."""
    csv_path = "/home/user/training_data.csv"
    assert os.path.exists(csv_path), f"{csv_path} does not exist."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, "training_data.csv is empty."

        assert header == ["x", "y", "label"], f"CSV header is incorrect. Expected ['x', 'y', 'label'], got: {header}"

        rows = list(reader)
        expected_rows = 80 * 80
        assert len(rows) == expected_rows, f"CSV should have {expected_rows} data rows, got {len(rows)}."

        # Validate a sample of the rows
        for row in rows[:100] + rows[-100:]:
            assert len(row) == 3, f"Row does not have exactly 3 columns: {row}"
            try:
                x, y, label = float(row[0]), float(row[1]), int(row[2])
            except ValueError:
                assert False, f"Could not parse row values as numbers: {row}"

            expected_label = 1 if (x**2 + y**2) <= 1.0 else 0
            assert label == expected_label, f"Incorrect label for point ({x}, {y}). Expected {expected_label}, got {label}."