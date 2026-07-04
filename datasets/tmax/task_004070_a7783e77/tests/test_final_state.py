# test_final_state.py

import os
import subprocess
import pytest

def test_video_frames_extracted():
    frames_dir = "/home/user/dataset/frames"
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} does not exist."

    files = os.listdir(frames_dir)
    jpg_files = [f for f in files if f.endswith(".jpg")]

    expected_frames = [f"frame_{i:04d}.jpg" for i in range(1, 13)]

    missing = set(expected_frames) - set(jpg_files)
    extra = set(jpg_files) - set(expected_frames)

    assert not missing, f"Missing expected frames: {sorted(list(missing))}"
    assert not extra, f"Found unexpected extra frames: {sorted(list(extra))}"
    assert len(jpg_files) == 12, f"Expected exactly 12 frames, found {len(jpg_files)}"

def get_script_path():
    py_script = "/home/user/backup_filter.py"
    sh_script = "/home/user/backup_filter.sh"
    if os.path.isfile(py_script):
        return py_script
    elif os.path.isfile(sh_script):
        return sh_script
    return None

def test_filter_script_exists_and_executable():
    script_path = get_script_path()
    assert script_path is not None, "Backup filter script not found at /home/user/backup_filter.py or /home/user/backup_filter.sh"
    assert os.access(script_path, os.X_OK) or script_path.endswith('.py'), f"Script {script_path} is not executable."

def run_filter_script(corpus_path):
    script_path = get_script_path()

    cmd = [script_path, corpus_path]
    if script_path.endswith('.py') and not os.access(script_path, os.X_OK):
        cmd = ["python3", script_path, corpus_path]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStderr: {result.stderr}"
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except subprocess.TimeoutExpired:
        pytest.fail("Script exceeded 10-second timeout, likely caught in an infinite loop.")

def test_clean_corpus_preserved():
    clean_dir = "/app/corpora/clean"
    output_lines = run_filter_script(clean_dir)

    expected_paths = []
    for root, dirs, files in os.walk(clean_dir):
        expected_paths.append(os.path.abspath(root))
        for d in dirs:
            expected_paths.append(os.path.abspath(os.path.join(root, d)))
        for f in files:
            expected_paths.append(os.path.abspath(os.path.join(root, f)))

    expected_paths = list(set(expected_paths))
    output_set = set(output_lines)

    missing = [p for p in expected_paths if p not in output_set]

    if missing:
        basenames = [os.path.basename(p) for p in missing]
        pytest.fail(f"{len(missing)} of {len(expected_paths)} clean modified/omitted. Offending: {basenames}")

def test_evil_corpus_filtered():
    evil_dir = "/app/corpora/evil"
    output_lines = run_filter_script(evil_dir)
    output_set = set(output_lines)

    evil_symlinks = [
        "loop1",
        "loop2",
        "loop3",
        "loop_dir/cyclic_sub",
        "escape_root",
        "escape_relative"
    ]

    evil_paths = [os.path.abspath(os.path.join(evil_dir, p)) for p in evil_symlinks]

    bypassed = [p for p in evil_paths if p in output_set]

    if bypassed:
        basenames = [os.path.basename(p) for p in bypassed]
        pytest.fail(f"{len(bypassed)} of {len(evil_paths)} evil bypassed. Offending: {basenames}")

    # Also ensure safe files in evil corpus are preserved
    safe_paths = [
        os.path.abspath(evil_dir),
        os.path.abspath(os.path.join(evil_dir, "valid_file.txt")),
        os.path.abspath(os.path.join(evil_dir, "loop_dir"))
    ]

    missing_safe = [p for p in safe_paths if p not in output_set]
    if missing_safe:
        basenames = [os.path.basename(p) for p in missing_safe]
        pytest.fail(f"{len(missing_safe)} of {len(safe_paths)} clean modified/omitted in evil dir. Offending: {basenames}")