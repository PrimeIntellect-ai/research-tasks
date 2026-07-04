# test_final_state.py

import os
import subprocess
import json
import shutil
import tempfile
import pytest

def get_actual_frame_count(video_path):
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-select_streams", "v:0", 
        "-count_frames", 
        "-show_entries", "stream=nb_read_frames", 
        "-of", "default=nokey=1:noprint_wrappers=1", 
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip().isdigit():
        return int(result.stdout.strip())
    return 144  # fallback to truth if ffprobe fails for some reason

def test_video_artifact_processing():
    frame_count_file = "/home/user/frame_count.txt"
    assert os.path.isfile(frame_count_file), f"Missing file: {frame_count_file}"

    expected_frames = get_actual_frame_count("/app/security_cam.mp4")

    with open(frame_count_file, "r") as f:
        content = f.read().strip()

    assert content == str(expected_frames), f"Expected frame count {expected_frames}, but got {content}"

def test_environment_variables_setup():
    profile_path = "/home/user/.profile"
    assert os.path.isfile(profile_path), f"Missing file: {profile_path}"

    expected_frames = get_actual_frame_count("/app/security_cam.mp4")

    with open(profile_path, "r") as f:
        content = f.read()

    assert "export PROXY_UPSTREAM=127.0.0.1:8080" in content or 'export PROXY_UPSTREAM="127.0.0.1:8080"' in content, \
        "PROXY_UPSTREAM variable not correctly exported in .profile"

    expected_export = f"export VIDEO_PROCESSED_COUNT={expected_frames}"
    assert expected_export in content or f'export VIDEO_PROCESSED_COUNT="{expected_frames}"' in content, \
        f"VIDEO_PROCESSED_COUNT variable not correctly exported in .profile. Expected to find: {expected_export}"

def test_adversarial_payload_sanitizer():
    script_path = "/home/user/filter_payloads.py"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    clean_corpus_dir = "/app/corpus/clean"
    evil_corpus_dir = "/app/corpus/evil"

    # Test clean corpus
    with tempfile.TemporaryDirectory() as tmp_clean_out:
        result = subprocess.run(["python3", script_path, clean_corpus_dir, tmp_clean_out], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on clean corpus: {result.stderr}"

        expected_clean_files = set(os.listdir(clean_corpus_dir))
        actual_clean_files = set(os.listdir(tmp_clean_out))

        missing_clean = expected_clean_files - actual_clean_files
        assert not missing_clean, f"{len(missing_clean)} of {len(expected_clean_files)} clean files modified/rejected: {', '.join(missing_clean)}"

        for f in expected_clean_files:
            with open(os.path.join(clean_corpus_dir, f), "r") as src, open(os.path.join(tmp_clean_out, f), "r") as dst:
                assert src.read() == dst.read(), f"Clean file {f} was modified during copy"

    # Test evil corpus
    with tempfile.TemporaryDirectory() as tmp_evil_out:
        result = subprocess.run(["python3", script_path, evil_corpus_dir, tmp_evil_out], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed on evil corpus: {result.stderr}"

        actual_evil_files = set(os.listdir(tmp_evil_out))
        assert not actual_evil_files, f"{len(actual_evil_files)} of {len(os.listdir(evil_corpus_dir))} evil files bypassed: {', '.join(actual_evil_files)}"

def test_mount_fstab_configuration():
    fstab_path = "/home/user/container_fstab"
    assert os.path.isfile(fstab_path), f"Missing file: {fstab_path}"

    clean_corpus_dir = "/app/corpus/clean"
    expected_mounts = []
    if os.path.isdir(clean_corpus_dir):
        for f in os.listdir(clean_corpus_dir):
            if f.endswith(".json"):
                with open(os.path.join(clean_corpus_dir, f), "r") as fp:
                    data = json.load(fp)
                    if "mount_path" in data:
                        expected_mounts.append(data["mount_path"])

    with open(fstab_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for mount_path in expected_mounts:
        expected_line = f"tmpfs {mount_path} tmpfs defaults 0 0"
        assert expected_line in lines, f"Missing expected fstab entry: {expected_line}"

def test_nginx_configuration():
    nginx_conf = "/home/user/nginx.conf"
    assert os.path.isfile(nginx_conf), f"Missing file: {nginx_conf}"

    # Test valid configuration
    result = subprocess.run(["nginx", "-t", "-c", nginx_conf], capture_output=True, text=True)
    assert result.returncode == 0, f"Nginx configuration failed validation:\n{result.stderr}"

    with open(nginx_conf, "r") as f:
        content = f.read()

    # Basic checks
    assert "9090" in content, "Nginx config does not appear to listen on port 9090"
    assert "proxy_pass http://127.0.0.1:8080" in content or "proxy_pass http://127.0.0.1:8080/" in content, \
        "Nginx config is missing the correct proxy_pass directive"
    assert "403" in content, "Nginx config is missing 403 Forbidden directive for missing/invalid header"
    assert "http_x_microservice" in content.lower() or "http_x_microservice" in content, \
        "Nginx config does not check the X-Microservice header"
    assert "accepted" in content, "Nginx config does not check for the 'accepted' value in the header"