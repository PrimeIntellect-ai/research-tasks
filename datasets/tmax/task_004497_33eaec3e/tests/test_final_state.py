# test_final_state.py
import os
import subprocess
import tempfile
import shutil
import pytest

def test_storage_setup():
    assert os.path.isfile("/home/user/alert_volume.img"), "/home/user/alert_volume.img does not exist"

    # Check if fuse2fs is mounted
    mount_output = subprocess.run(["mount"], capture_output=True, text=True).stdout
    assert "/home/user/alert_data" in mount_output or "fuse2fs" in mount_output, "/home/user/alert_data is not mounted"

    assert os.path.islink("/home/user/current_alerts"), "/home/user/current_alerts is not a symlink"
    assert os.readlink("/home/user/current_alerts") == "/home/user/alert_data/incoming", "Symlink does not point to /home/user/alert_data/incoming"

    for d in ["incoming", "processing", "archive"]:
        assert os.path.isdir(f"/home/user/alert_data/{d}"), f"Directory /home/user/alert_data/{d} does not exist"

def test_rust_binary_adversarial_corpus():
    binary_path_release = "/home/user/alert_classifier/target/release/alert-filter"
    binary_path_debug = "/home/user/alert_classifier/target/debug/alert-filter"

    if os.path.isfile(binary_path_release):
        binary = binary_path_release
    elif os.path.isfile(binary_path_debug):
        binary = binary_path_debug
    else:
        pytest.fail("Rust binary alert-filter not found in release or debug target directories")

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".txt")]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".txt")]

    failed_clean = []
    failed_evil = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for cf in clean_files:
            input_file = os.path.join(clean_dir, cf)
            res = subprocess.run([binary, input_file, tmpdir], capture_output=True)
            if res.returncode != 0:
                failed_clean.append(cf)
            elif not os.path.isfile(os.path.join(tmpdir, cf)):
                failed_clean.append(cf + " (not copied)")

        for ef in evil_files:
            input_file = os.path.join(evil_dir, ef)
            res = subprocess.run([binary, input_file, tmpdir], capture_output=True)
            if res.returncode != 1:
                failed_evil.append(ef)

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}"
    assert not failed_evil, f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}"

def test_audio_transcription():
    transcript_path = "/home/user/alert_data/archive/sample_transcript.txt"
    assert os.path.isfile(transcript_path), f"Transcript not found at {transcript_path}"
    with open(transcript_path, "r") as f:
        content = f.read().strip().lower()
    expected = "warning. database shard seven has reached maximum iops capacity."
    assert expected in content, f"Transcript content incorrect. Got: {content}"

def test_service_management():
    res = subprocess.run(["systemctl", "--user", "is-active", "alert-processor.timer"], capture_output=True, text=True)
    assert res.stdout.strip() == "active", "alert-processor.timer is not active"

def test_final_output():
    status_file = "/home/user/status.log"
    assert os.path.isfile(status_file), f"Status file {status_file} not found"
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert content == "PIPELINE ACTIVE", f"Status file content incorrect. Got: {content}"