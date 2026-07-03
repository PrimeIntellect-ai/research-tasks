# test_final_state.py

import os
import pytest

def test_extraction_completed():
    raw_data_dir = "/home/user/raw_data"
    assert os.path.isdir(raw_data_dir), f"Directory {raw_data_dir} does not exist. Did you extract the archive?"
    assert os.path.isfile(os.path.join(raw_data_dir, "dataset.ini")), "dataset.ini is missing from raw_data."

    expected_files = ["file_a.dat", "file_b.dat", "file_c.dat", "file_d.dat", "file_e.dat"]
    for f in expected_files:
        assert os.path.isfile(os.path.join(raw_data_dir, f)), f"Expected file {f} is missing from raw_data."

def test_symlinks_created_correctly():
    organized_dir = "/home/user/organized_dataset"
    assert os.path.isdir(organized_dir), f"Directory {organized_dir} does not exist."

    expected_symlinks = {
        "Subject_Argon.dat": "/home/user/raw_data/file_b.dat",
        "Subject_Krypton.dat": "/home/user/raw_data/file_c.dat",
        "Subject_Radon.dat": "/home/user/raw_data/file_e.dat",
        "Subject_Xenon.dat": "/home/user/raw_data/file_a.dat"
    }

    # Check that only the expected symlinks exist
    actual_files = set(os.listdir(organized_dir))
    expected_files = set(expected_symlinks.keys())
    assert actual_files == expected_files, f"Expected symlinks {expected_files}, but found {actual_files}"

    for symlink_name, target_path in expected_symlinks.items():
        symlink_path = os.path.join(organized_dir, symlink_name)
        assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

        actual_target = os.readlink(symlink_path)
        assert actual_target == target_path, f"Symlink {symlink_name} points to {actual_target}, expected {target_path}. Note: target must be absolute."

def test_report_csv_correct():
    report_path = "/home/user/report.csv"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    expected_lines = [
        "Subject_Argon,/home/user/raw_data/file_b.dat",
        "Subject_Krypton,/home/user/raw_data/file_c.dat",
        "Subject_Radon,/home/user/raw_data/file_e.dat",
        "Subject_Xenon,/home/user/raw_data/file_a.dat"
    ]

    with open(report_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Report content is incorrect. Expected:\n{expected_lines}\nGot:\n{actual_lines}"