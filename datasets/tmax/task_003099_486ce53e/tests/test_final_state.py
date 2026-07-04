# test_final_state.py

import os
import glob
import subprocess
import gzip
import tempfile

def test_video_frames_extracted():
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} does not exist."

    frames = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
    assert len(frames) == 15, f"Expected 15 frames, found {len(frames)}."

    for i in range(1, 16):
        expected_name = f"frame_{i:03d}.jpg"
        assert os.path.basename(frames[i-1]) == expected_name, f"Expected frame name {expected_name}, found {os.path.basename(frames[i-1])}."

def test_frame_count_file():
    count_file = "/home/user/frame_count.txt"
    assert os.path.isfile(count_file), f"File {count_file} does not exist."

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "15", f"Expected frame count to be '15', found '{content}'."

def test_sanitizer_executable_exists():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Executable {sanitizer_path} does not exist."
    assert os.access(sanitizer_path, os.X_OK), f"{sanitizer_path} is not executable."

def get_records(text):
    records = []
    current_record = []
    in_record = False
    for line in text.splitlines(keepends=True):
        if line.strip() == "BEGIN_RECORD":
            in_record = True
            current_record = [line]
        elif line.strip() == "END_RECORD" and in_record:
            current_record.append(line)
            records.append("".join(current_record))
            in_record = False
            current_record = []
        elif in_record:
            current_record.append(line)
    return records

def test_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/sanitizer"
    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.log.gz"))

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for clean_file in clean_files:
            out_file = os.path.join(tmpdir, os.path.basename(clean_file).replace(".log.gz", ".log"))
            result = subprocess.run([sanitizer_path, clean_file, out_file], capture_output=True)

            if result.returncode != 0:
                failed_files.append(f"{os.path.basename(clean_file)} (exit code {result.returncode})")
                continue

            with gzip.open(clean_file, "rt", encoding="utf-8") as f:
                expected_content = f.read()

            if not os.path.isfile(out_file):
                failed_files.append(f"{os.path.basename(clean_file)} (output file not created)")
                continue

            with open(out_file, "r", encoding="utf-8") as f:
                actual_content = f.read()

            if expected_content != actual_content:
                failed_files.append(f"{os.path.basename(clean_file)} (content mismatch)")

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified or failed: " + ", ".join(failed_files)

def test_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/sanitizer"
    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.log.gz"))

    failed_files = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for evil_file in evil_files:
            out_file = os.path.join(tmpdir, os.path.basename(evil_file).replace(".log.gz", ".log"))
            result = subprocess.run([sanitizer_path, evil_file, out_file], capture_output=True)

            if result.returncode != 1:
                failed_files.append(f"{os.path.basename(evil_file)} (exit code {result.returncode} instead of 1)")
                continue

            with gzip.open(evil_file, "rt", encoding="utf-8") as f:
                original_content = f.read()

            expected_records = []
            for record in get_records(original_content):
                if "../" not in record and "MALICIOUS" not in record:
                    expected_records.append(record)
            expected_content = "".join(expected_records)

            if not os.path.isfile(out_file):
                failed_files.append(f"{os.path.basename(evil_file)} (output file not created)")
                continue

            with open(out_file, "r", encoding="utf-8") as f:
                actual_content = f.read()

            if expected_content != actual_content:
                failed_files.append(f"{os.path.basename(evil_file)} (content mismatch)")

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed or failed: " + ", ".join(failed_files)