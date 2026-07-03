# test_final_state.py

import os
import stat
import csv

def test_script_exists_and_executable():
    script_path = "/home/user/organize.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a regular file."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Script {script_path} is not executable by the user."

def test_directories_created():
    alpha_dir = "/home/user/clean_data/alpha_exp"
    beta_dir = "/home/user/clean_data/beta_exp"
    assert os.path.isdir(alpha_dir), f"Directory {alpha_dir} does not exist."
    assert os.path.isdir(beta_dir), f"Directory {beta_dir} does not exist."

def test_json_to_csv_conversion():
    csv_path = "/home/user/clean_data/alpha_exp/results.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a regular file."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 3, f"{csv_path} should have a header and at least 2 rows of data."

    # Check headers
    header = [col.strip('"\' ') for col in rows[0]]
    assert set(header) == {"timestamp", "sensor", "reading"}, f"Header row in {csv_path} does not match expected keys."

    # Check data content
    data_str = " ".join("".join(row) for row in rows[1:])
    assert "1620000000" in data_str, "Missing timestamp 1620000000 in CSV."
    assert "45.2" in data_str, "Missing reading 45.2 in CSV."
    assert "1620000060" in data_str, "Missing timestamp 1620000060 in CSV."
    assert "46.1" in data_str, "Missing reading 46.1 in CSV."
    assert "A" in data_str.replace('"', ''), "Missing sensor A in CSV."

def test_hardlink_created():
    source_path = "/home/user/raw_data/beta.csv"
    target_path = "/home/user/clean_data/beta_exp/results.csv"

    assert os.path.exists(source_path), f"Source file {source_path} is missing."
    assert os.path.exists(target_path), f"Target file {target_path} does not exist."

    stat_source = os.stat(source_path)
    stat_target = os.stat(target_path)

    assert stat_source.st_ino == stat_target.st_ino, f"{target_path} is not a hard link to {source_path} (inodes differ)."

def test_symlink_latest_dataset():
    symlink_path = "/home/user/clean_data/latest_dataset"
    expected_target = "/home/user/clean_data/alpha_exp"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    actual_target = os.readlink(symlink_path)
    assert actual_target == expected_target, f"Symlink points to {actual_target}, expected {expected_target}."