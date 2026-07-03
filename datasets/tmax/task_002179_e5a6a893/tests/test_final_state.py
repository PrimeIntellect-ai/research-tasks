# test_final_state.py

import os
import subprocess
import json
import pytest

def get_video_info(path):
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", path]
    output = subprocess.check_output(cmd)
    info = json.loads(output)
    stream = info['streams'][0]
    return int(stream['width']), int(stream['height'])

def count_blue_frames(path):
    w, h = get_video_info(path)
    frame_size = w * h * 3
    cmd = ["ffmpeg", "-i", path, "-f", "image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    blue_count = 0
    expected_frame = b'\x00\x00\xff' * (w * h)

    while True:
        frame = proc.stdout.read(frame_size)
        if not frame or len(frame) < frame_size:
            break
        if frame == expected_frame:
            blue_count += 1

    proc.stdout.close()
    proc.wait()
    return blue_count

def simulate_sanitizer(input_text, N):
    lines = input_text.split('\n')
    output_lines = []
    last_seen = {}

    for line in lines:
        if not line:
            continue
        parts = line.split(',')
        if len(parts) != 4:
            continue
        ts_str, vid_str, speed_str, lp = parts
        try:
            ts = int(ts_str)
            vid = int(vid_str)
        except ValueError:
            continue

        # Validate LP: only A-Z, 0-9, -
        if not all(c.isupper() or c.isdigit() or c == '-' for c in lp):
            continue

        # Dedup: within N seconds of the most recent accepted record
        if vid in last_seen and abs(ts - last_seen[vid]) <= N:
            continue

        last_seen[vid] = ts

        # Mask LP
        if len(lp) <= 2:
            masked_lp = lp
        else:
            masked_lp = '*' * (len(lp) - 2) + lp[-2:]

        output_lines.append(f"{ts},{vid},{speed_str},{masked_lp}")

    if not output_lines:
        return ""
    return "\n".join(output_lines) + "\n"

@pytest.fixture(scope="session")
def deduplication_window():
    video_path = "/app/fault_log.mp4"
    assert os.path.exists(video_path), f"Video file missing at {video_path}"
    return count_blue_frames(video_path)

@pytest.fixture(scope="session")
def sanitizer_executable():
    exe_path = "/home/user/sanitizer"
    assert os.path.exists(exe_path), f"Executable missing at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"
    return exe_path

def run_sanitizer(executable, input_text):
    proc = subprocess.run(
        [executable],
        input=input_text,
        text=True,
        capture_output=True,
        timeout=5
    )
    assert proc.returncode == 0, f"Sanitizer crashed or failed with return code {proc.returncode}"
    return proc.stdout

def test_clean_corpus(sanitizer_executable, deduplication_window):
    clean_dir = "/app/corpus/clean/"
    assert os.path.exists(clean_dir), "Clean corpus directory missing"

    files = [f for f in os.listdir(clean_dir) if f.endswith(".csv")]
    assert len(files) > 0, "No CSV files found in clean corpus"

    failed_files = []

    for filename in files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "r") as f:
            input_data = f.read()

        expected_output = simulate_sanitizer(input_data, deduplication_window)
        actual_output = run_sanitizer(sanitizer_executable, input_data)

        if actual_output != expected_output:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(files)} clean modified or processed incorrectly: {', '.join(failed_files)}"

def test_evil_corpus(sanitizer_executable, deduplication_window):
    evil_dir = "/app/corpus/evil/"
    assert os.path.exists(evil_dir), "Evil corpus directory missing"

    files = [f for f in os.listdir(evil_dir) if f.endswith(".csv")]
    assert len(files) > 0, "No CSV files found in evil corpus"

    failed_files = []

    for filename in files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "r") as f:
            input_data = f.read()

        expected_output = simulate_sanitizer(input_data, deduplication_window)

        try:
            actual_output = run_sanitizer(sanitizer_executable, input_data)
            if actual_output != expected_output:
                failed_files.append(filename)
        except Exception:
            # Crashes are considered bypasses/failures
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(files)} evil bypassed or crashed: {', '.join(failed_files)}"