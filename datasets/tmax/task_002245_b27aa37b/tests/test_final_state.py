# test_final_state.py
import os
import zipfile
import glob

def test_largest_backups_output():
    output_file = "/home/user/largest_backups.txt"
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist."

    # Derive expected output
    backup_dir = "/home/user/backups"
    zip_files = glob.glob(os.path.join(backup_dir, "*.zip"))

    results = []
    for zf_path in zip_files:
        if not zipfile.is_zipfile(zf_path):
            continue
        try:
            with zipfile.ZipFile(zf_path, 'r') as zf:
                infolist = zf.infolist()
                if not infolist:
                    continue
                max_size = max(info.file_size for info in infolist)
                results.append((zf_path, max_size))
        except zipfile.BadZipFile:
            continue

    # Sort descending by size
    results.sort(key=lambda x: x[1], reverse=True)

    expected_lines = [f"{path}: {size}" for path, size in results]

    with open(output_file, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Output file has {len(actual_lines)} lines, expected {len(expected_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} mismatch.\n"
            f"Expected: '{expected}'\n"
            f"Actual:   '{actual}'"
        )