# test_final_state.py

import os
import subprocess
from pathlib import Path

def test_frame_count():
    frame_count_file = Path("/home/user/frame_count.txt")
    assert frame_count_file.is_file(), f"Missing frame count file: {frame_count_file}"
    content = frame_count_file.read_text().strip()
    assert content == "12", f"Expected frame count to be '12', but got '{content}'."

def test_alert_routes():
    routes_file = Path("/home/user/alert_routes.conf")
    assert routes_file.is_file(), f"Missing routes config file: {routes_file}"
    lines = [line.strip() for line in routes_file.read_text().strip().splitlines() if line.strip()]
    expected_lines = [
        "10.50.0.0/16 via 192.168.1.254",
        "0.0.0.0/0 via 192.168.1.1"
    ]
    assert lines == expected_lines, f"Routes config does not match expected. Got: {lines}"

def test_pipeline_exists_executable():
    pipeline_file = Path("/home/user/pipeline.sh")
    assert pipeline_file.is_file(), f"Missing pipeline script: {pipeline_file}"
    assert os.access(pipeline_file, os.X_OK), f"Pipeline script is not executable: {pipeline_file}"

def test_verified_maildir():
    maildir = Path("/home/user/verified_maildir/new")
    assert maildir.is_dir(), f"Missing verified maildir: {maildir}"

    files = list(maildir.iterdir())
    assert len(files) == 1, f"Expected exactly 1 file in {maildir}, found {len(files)}"

    clean_eml_path = maildir / "clean1.eml"
    if not clean_eml_path.exists():
        # If the file has a different name, check its content
        file_content = files[0].read_text().strip()
        expected_content = Path("/app/incoming_alerts/clean1.eml").read_text().strip()
        assert file_content == expected_content, f"File in maildir does not match clean1.eml content. Got: {file_content}"

def test_alert_filter_eval_corpus():
    filter_script = Path("/home/user/alert_filter.sh")
    assert filter_script.is_file(), f"Missing alert filter script: {filter_script}"
    assert os.access(filter_script, os.X_OK), f"Alert filter script is not executable: {filter_script}"

    clean_corpus_dir = Path("/app/eval_corpora/clean_alerts")
    evil_corpus_dir = Path("/app/eval_corpora/evil_alerts")

    clean_modified = []
    for clean_file in clean_corpus_dir.iterdir():
        if clean_file.is_file():
            result = subprocess.run([str(filter_script), str(clean_file)], capture_output=True)
            if result.returncode != 0:
                clean_modified.append(clean_file.name)

    evil_bypassed = []
    for evil_file in evil_corpus_dir.iterdir():
        if evil_file.is_file():
            result = subprocess.run([str(filter_script), str(evil_file)], capture_output=True)
            if result.returncode == 0:
                evil_bypassed.append(evil_file.name)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(list(evil_corpus_dir.iterdir()))} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(list(clean_corpus_dir.iterdir()))} clean modified/rejected: {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus verification failed:\n" + "\n".join(errors)