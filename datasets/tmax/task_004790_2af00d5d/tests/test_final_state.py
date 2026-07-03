# test_final_state.py

import os
import csv
import re
import subprocess
import tempfile
import filecmp

def get_expected_rows(input_csv):
    expected_rows = []
    # Strict regex for ISO 8601 timestamp as per example YYYY-MM-DDTHH:MM:SSZ
    timestamp_regex = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
    sensor_id_regex = re.compile(r'^[A-Z]{3}-\d{4}(-[A-Z])?$')

    with open(input_csv, 'r', newline='', encoding='utf-8') as f:
        content = f.read()

    # We need to parse the CSV properly, handling embedded newlines
    # csv.reader handles it if we pass the file object
    with open(input_csv, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return []

        expected_rows.append(headers)

        # Find column indices
        try:
            timestamp_idx = headers.index('timestamp')
            sensor_id_idx = headers.index('sensor_id')
        except ValueError:
            # If standard headers are missing, we might not be able to filter properly
            # Assuming standard structure based on task description
            timestamp_idx = 0
            sensor_id_idx = 1

        for row in reader:
            # Check 1: Embedded newlines anywhere in the row
            has_newline = any('\n' in cell or '\r' in cell for cell in row)
            if has_newline:
                continue

            # Check 2: Timestamp format
            if timestamp_idx < len(row):
                if not timestamp_regex.match(row[timestamp_idx]):
                    continue
            else:
                continue

            # Check 3: Sensor ID regex
            if sensor_id_idx < len(row):
                if not sensor_id_regex.match(row[sensor_id_idx]):
                    continue
            else:
                continue

            expected_rows.append(row)

    return expected_rows

def test_sanitizer_on_clean_corpus():
    clean_dir = "/app/corpora/clean/"
    sanitizer_script = "/home/user/sanitizer.py"

    assert os.path.isfile(sanitizer_script), f"Sanitizer script missing at {sanitizer_script}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    if not clean_files:
        pytest.skip("No clean CSVs found to test.")

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for fname in clean_files:
            input_path = os.path.join(clean_dir, fname)
            output_path = os.path.join(tmpdir, fname)

            subprocess.run(["python3", sanitizer_script, input_path, output_path], capture_output=True)

            if not os.path.exists(output_path):
                failed_files.append(fname)
                continue

            # Clean files should be perfectly preserved
            with open(input_path, 'r', newline='', encoding='utf-8') as f1, \
                 open(output_path, 'r', newline='', encoding='utf-8') as f2:
                if f1.read() != f2.read():
                    failed_files.append(fname)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified or failed: {', '.join(failed_files)}"

def test_sanitizer_on_evil_corpus():
    evil_dir = "/app/corpora/evil/"
    sanitizer_script = "/home/user/sanitizer.py"

    assert os.path.isfile(sanitizer_script), f"Sanitizer script missing at {sanitizer_script}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    if not evil_files:
        pytest.skip("No evil CSVs found to test.")

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for fname in evil_files:
            input_path = os.path.join(evil_dir, fname)
            output_path = os.path.join(tmpdir, fname)

            subprocess.run(["python3", sanitizer_script, input_path, output_path], capture_output=True)

            if not os.path.exists(output_path):
                failed_files.append(fname)
                continue

            expected_rows = get_expected_rows(input_path)

            with open(output_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                actual_rows = list(reader)

            if actual_rows != expected_rows:
                failed_files.append(fname)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed or improperly sanitized: {', '.join(failed_files)}"

def test_pipeline_orchestration():
    pipeline_script = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_script), f"Pipeline script missing at {pipeline_script}"

    clean_dir = "/app/corpora/clean/"
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]

    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(["bash", pipeline_script, clean_dir, tmpdir], capture_output=True)
        assert result.returncode == 0, f"Pipeline script failed with error: {result.stderr.decode()}"

        report_path = os.path.join(tmpdir, "report.html")
        assert os.path.isfile(report_path), "HTML report was not generated at the output directory."

        with open(report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()

        assert "Sanitization Complete" in report_content, "Report missing exact string 'Sanitization Complete'."
        assert str(len(clean_files)) in report_content, "Report does not seem to list the correct number of files processed."

        output_csvs = [f for f in os.listdir(tmpdir) if f.endswith('.csv')]
        assert len(output_csvs) == len(clean_files), "Output directory does not contain the same number of CSV files as the input."