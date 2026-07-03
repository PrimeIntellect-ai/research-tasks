# test_final_state.py

import os
import tarfile

def test_c_program_exists():
    """Verify that the C source code file was created."""
    c_file = "/home/user/process_data.c"
    assert os.path.isfile(c_file), f"C source file missing at {c_file}"

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    exe_file = "/home/user/process_data"
    assert os.path.isfile(exe_file), f"Executable missing at {exe_file}"
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable"

def test_filtered_dataset_csv():
    """Verify the contents of the filtered dataset CSV."""
    csv_file = "/home/user/filtered_dataset.csv"
    assert os.path.isfile(csv_file), f"Filtered dataset missing at {csv_file}"

    with open(csv_file, "r", encoding="utf-8") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "ID,Timestamp,Sensor,Value,Notes",
        "2,2023-01-01T10:05,TEMP_01,26.1,High",
        "5,2023-01-01T10:20,TEMP_01,28.4,Critical",
        "7,2023-01-01T10:30,TEMP_01,25.5,High"
    ]

    assert content == expected_content, "The filtered dataset does not contain the expected rows or header."

def test_summary_txt():
    """Verify the contents of the summary text file."""
    summary_file = "/home/user/summary.txt"
    assert os.path.isfile(summary_file), f"Summary file missing at {summary_file}"

    with open(summary_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == "Filtered rows: 3", f"Summary file content is incorrect: {content}"

def test_processed_dataset_tar_gz():
    """Verify the processed dataset tarball exists and contains the correct files at the root."""
    archive_path = "/home/user/processed_dataset.tar.gz"
    assert os.path.isfile(archive_path), f"Processed dataset archive missing at {archive_path}"
    assert tarfile.is_tarfile(archive_path), f"The file {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        assert "filtered_dataset.csv" in names, "filtered_dataset.csv is missing from the root of the archive."
        assert "summary.txt" in names, "summary.txt is missing from the root of the archive."

        # Ensure no parent directories are included
        assert "/home/user/filtered_dataset.csv" not in names, "Archive should not contain absolute paths or parent directories."
        assert "home/user/filtered_dataset.csv" not in names, "Archive should not contain the home/user directory structure."

        # Verify contents inside the tarball
        csv_member = tar.extractfile("filtered_dataset.csv")
        assert csv_member is not None, "Could not extract filtered_dataset.csv from archive."
        csv_content = csv_member.read().decode("utf-8").strip().splitlines()
        expected_csv = [
            "ID,Timestamp,Sensor,Value,Notes",
            "2,2023-01-01T10:05,TEMP_01,26.1,High",
            "5,2023-01-01T10:20,TEMP_01,28.4,Critical",
            "7,2023-01-01T10:30,TEMP_01,25.5,High"
        ]
        assert csv_content == expected_csv, "The filtered_dataset.csv inside the archive does not match expected contents."

        txt_member = tar.extractfile("summary.txt")
        assert txt_member is not None, "Could not extract summary.txt from archive."
        txt_content = txt_member.read().decode("utf-8").strip()
        assert txt_content == "Filtered rows: 3", "The summary.txt inside the archive does not match expected contents."