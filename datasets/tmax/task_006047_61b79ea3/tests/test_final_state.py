# test_final_state.py
import os

def test_extracted_files_renamed():
    extracted_dir = "/home/user/extracted"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist"

    expected_files = {
        "patient_x_read1.fq",
        "patient_x_read2.fq",
        "patient_y_read1.fq",
        "patient_y_read2.fq",
        "unmapped_data.txt"
    }

    actual_files = set(os.listdir(extracted_dir))

    missing_files = expected_files - actual_files
    unexpected_files = actual_files - expected_files

    assert not missing_files, f"Missing expected files in {extracted_dir}: {missing_files}"
    assert not unexpected_files, f"Unexpected files found in {extracted_dir} (did not rename correctly or extracted extra files): {unexpected_files}"

def test_rename_log_contents():
    log_file = "/home/user/rename_log.txt"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist"

    expected_lines = {
        "RENAMED: sample1_read1.fq -> patient_x_read1.fq",
        "RENAMED: sample1_read2.fq -> patient_x_read2.fq",
        "RENAMED: sample2_read1.fq -> patient_y_read1.fq",
        "RENAMED: sample2_read2.fq -> patient_y_read2.fq"
    }

    with open(log_file, "r") as f:
        actual_lines = {line.strip() for line in f if line.strip()}

    missing_lines = expected_lines - actual_lines
    unexpected_lines = actual_lines - expected_lines

    assert not missing_lines, f"Missing expected log lines: {missing_lines}"
    assert not unexpected_lines, f"Unexpected log lines found: {unexpected_lines}"

def test_python_script_exists():
    script_file = "/home/user/rename.py"
    assert os.path.isfile(script_file), f"Python script {script_file} does not exist"