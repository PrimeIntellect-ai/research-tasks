# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect_stutter.py"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def run_classifier(video_path):
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, video_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return None, f"Script exited with code {result.returncode}. Stderr: {result.stderr.strip()}"
        output = result.stdout.strip()
        return output, None
    except subprocess.TimeoutExpired:
        return None, "Script timed out after 30 seconds."
    except Exception as e:
        return None, f"Execution error: {str(e)}"

def test_classifier_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_adversarial_corpus():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    clean_videos = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.mp4')]
    evil_videos = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.mp4')]

    assert len(clean_videos) > 0, "No clean videos found to test."
    assert len(evil_videos) > 0, "No evil videos found to test."

    clean_failures = []
    evil_failures = []

    for video in clean_videos:
        output, err = run_classifier(video)
        if err:
            clean_failures.append((os.path.basename(video), err))
        elif output != "CLEAN":
            clean_failures.append((os.path.basename(video), f"Expected 'CLEAN', got '{output}'"))

    for video in evil_videos:
        output, err = run_classifier(video)
        if err:
            evil_failures.append((os.path.basename(video), err))
        elif output != "EVIL":
            evil_failures.append((os.path.basename(video), f"Expected 'EVIL', got '{output}'"))

    total_clean = len(clean_videos)
    total_evil = len(evil_videos)

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {total_clean} clean modified/failed:")
        for f, err in clean_failures:
            error_msg.append(f"  - {f}: {err}")

    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {total_evil} evil bypassed/failed:")
        for f, err in evil_failures:
            error_msg.append(f"  - {f}: {err}")

    if error_msg:
        pytest.fail("\n".join(error_msg))