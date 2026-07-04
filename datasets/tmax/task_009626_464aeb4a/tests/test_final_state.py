# test_final_state.py
import os

def test_plan_backups_script_exists_and_executable():
    script_path = "/home/user/plan_backups.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_backup_set_correct():
    output_path = "/home/user/backup_set.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_set = [
        "categories",
        "inventory",
        "orders",
        "permissions",
        "products",
        "roles",
        "users",
        "warehouses"
    ]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_set, (
        f"Contents of {output_path} are incorrect.\n"
        f"Expected: {expected_set}\n"
        f"Got: {actual_lines}"
    )

def test_core_table_correct():
    output_path = "/home/user/core_table.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        actual = f.read().strip()

    expected = "users"
    assert actual == expected, (
        f"Contents of {output_path} are incorrect. "
        f"Expected '{expected}', got '{actual}'."
    )