# test_final_state.py

import os
import tarfile
import struct

def get_expected_data():
    records = [
        ("rec_001", 104, 1680000000, [1.1111, 2.2222, 3.3333, 4.4444, 5.5555, 6.6666, 7.7777, 8.8888, 9.9999, 10.0000]),
        ("rec_002", 205, 1680003600, [0.0, -1.5, 3.1415, 2.7182, 42.0, 7.0, 8.0, 9.0, 10.1234, -5.5555]),
        ("rec_003", 99, 1680007200, [100.1, 200.2, 300.3, 400.4, 500.5, 600.6, 700.7, 800.8, 900.9, 1000.1]),
    ]
    expected = {}
    for name, sensor_id, ts, floats in records:
        # Simulate standard C float parsing and formatting to exactly 4 decimal places
        # by packing as 32-bit float and unpacking back to python float
        packed = struct.pack("<10f", *floats)
        unpacked = struct.unpack("<10f", packed)
        csv_line = ",".join(f"{v:.4f}" for v in unpacked)
        expected[name] = {
            "sensor_id": sensor_id,
            "ts": ts,
            "csv_line": csv_line,
            "txt_content": f"Notes for {name}\n",
            "base_name": f"sensor_{sensor_id}_{ts}"
        }
    return expected

def test_conversion_log():
    log_path = "/home/user/conversion.log"
    assert os.path.isfile(log_path), f"Missing log file: {log_path}"

    expected_data = get_expected_data()
    expected_lines = []
    for rec_name in sorted(expected_data.keys()):
        base_name = expected_data[rec_name]["base_name"]
        expected_lines.append(f"{rec_name} -> {base_name}\n")

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert lines == expected_lines, f"Log file contents do not match expected format or sorting. Found: {lines}"

def test_clean_dataset_tarball():
    tarball_path = "/home/user/clean_dataset.tar.gz"
    assert os.path.isfile(tarball_path), f"Missing clean dataset tarball: {tarball_path}"

    expected_data = get_expected_data()

    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            members = tar.getnames()

            for rec_name, data in expected_data.items():
                base_name = data["base_name"]
                csv_name = f"clean_data/{base_name}.csv"
                txt_name = f"clean_data/{base_name}.txt"

                # Allow for paths with or without leading './' or '/'
                csv_found = any(m.endswith(csv_name) for m in members)
                txt_found = any(m.endswith(txt_name) for m in members)

                assert csv_found, f"Missing {csv_name} in tarball"
                assert txt_found, f"Missing {txt_name} in tarball"

                # Check CSV content
                csv_member = next(m for m in tar.getmembers() if m.name.endswith(csv_name))
                with tar.extractfile(csv_member) as f:
                    csv_content = f.read().decode('utf-8').strip()
                    assert csv_content == data["csv_line"], f"CSV content mismatch in {csv_name}. Expected: {data['csv_line']}, Got: {csv_content}"

                # Check TXT content
                txt_member = next(m for m in tar.getmembers() if m.name.endswith(txt_name))
                with tar.extractfile(txt_member) as f:
                    txt_content = f.read().decode('utf-8')
                    assert txt_content == data["txt_content"], f"TXT content mismatch in {txt_name}."

    except tarfile.ReadError:
        assert False, f"{tarball_path} is not a valid gzip-compressed tarball"