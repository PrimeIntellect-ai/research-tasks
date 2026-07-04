# test_final_state.py
import os
import tarfile
import zipfile
import re
from datetime import datetime

def parse_records_from_tar(tar_path):
    records = []
    with tarfile.open(tar_path, "r:gz") as tar:
        members = [m for m in tar.getmembers() if m.isfile() and m.name.endswith('.log')]
        members.sort(key=lambda m: m.name)

        for member in members:
            f = tar.extractfile(member)
            content = f.read().decode('utf-8')

            raw_records = re.findall(r'===BEGIN_RECORD===\n(.*?)===END_RECORD===', content, re.DOTALL)
            for raw in raw_records:
                ts_match = re.search(r'Timestamp:\s*(\S+)', raw)
                status_match = re.search(r'Status:\s*(\S+)', raw)
                if ts_match and status_match:
                    records.append({
                        'ts': ts_match.group(1),
                        'status': status_match.group(1),
                        'raw': f"===BEGIN_RECORD===\n{raw}===END_RECORD===\n"
                    })
    return records

def format_ts(ts_str):
    dt = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y%m%d_%H%M%S")

def get_expected_chunks():
    tar_path = "/home/user/raw_data.tar.gz"
    assert os.path.exists(tar_path), f"Original archive {tar_path} is missing."

    all_records = parse_records_from_tar(tar_path)
    valid_records = [r for r in all_records if r['status'] == 'OK']

    chunks = []
    for i in range(0, len(valid_records), 10):
        chunks.append(valid_records[i:i+10])

    expected_files = {}
    for chunk in chunks:
        start_ts = format_ts(chunk[0]['ts'])
        end_ts = format_ts(chunk[-1]['ts'])
        filename = f"dataset_from_{start_ts}_to_{end_ts}.log"
        expected_files[filename] = chunk

    return expected_files

def test_clean_dataset_zip_exists():
    zip_path = "/home/user/clean_dataset.zip"
    assert os.path.exists(zip_path), f"Final zip archive {zip_path} was not created."
    assert zipfile.is_zipfile(zip_path), f"{zip_path} is not a valid zip file."

def test_processed_data_contents():
    zip_path = "/home/user/clean_dataset.zip"
    assert os.path.exists(zip_path), "Zip archive missing."

    expected_chunks = get_expected_chunks()

    with zipfile.ZipFile(zip_path, 'r') as z:
        zip_names = z.namelist()

        # Check that all files are under processed_data/
        for name in zip_names:
            if not name.endswith('/'):
                assert name.startswith("processed_data/"), f"File {name} in zip is not under 'processed_data/' directory."

        # Extract just the basenames for log files
        log_files_in_zip = {os.path.basename(name): name for name in zip_names if name.endswith('.log')}

        for expected_filename, chunk in expected_chunks.items():
            assert expected_filename in log_files_in_zip, f"Expected file {expected_filename} not found in the zip archive."

            zip_internal_path = log_files_in_zip[expected_filename]
            with z.open(zip_internal_path) as f:
                content = f.read().decode('utf-8')

                # Check counts
                begin_count = content.count("===BEGIN_RECORD===")
                assert begin_count == len(chunk), f"File {expected_filename} should have {len(chunk)} records, found {begin_count}."

                # Check for invalid statuses
                assert "Status: ERROR" not in content, f"File {expected_filename} contains an ERROR record."
                assert "Status: CALIBRATING" not in content, f"File {expected_filename} contains a CALIBRATING record."

def test_processed_data_directory():
    processed_dir = "/home/user/processed_data"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist."

    expected_chunks = get_expected_chunks()
    actual_files = [f for f in os.listdir(processed_dir) if f.endswith('.log')]

    for expected_filename, chunk in expected_chunks.items():
        assert expected_filename in actual_files, f"Expected file {expected_filename} not found in {processed_dir}."

        file_path = os.path.join(processed_dir, expected_filename)
        with open(file_path, 'r') as f:
            content = f.read()

            begin_count = content.count("===BEGIN_RECORD===")
            assert begin_count == len(chunk), f"File {expected_filename} should have {len(chunk)} records, found {begin_count}."

            assert "Status: ERROR" not in content, f"File {expected_filename} contains an ERROR record."
            assert "Status: CALIBRATING" not in content, f"File {expected_filename} contains a CALIBRATING record."