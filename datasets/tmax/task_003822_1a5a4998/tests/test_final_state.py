# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_vendored_package_fixed():
    makefile_path = "/app/vendor/github.com/buger/jsonparser/Makefile"
    assert os.path.exists(makefile_path), f"Makefile missing at {makefile_path}"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "GOOS=windows" not in content, "The vendored Makefile still contains the GOOS=windows perturbation."
    assert "BUILD_TAG=broken" not in content, "The vendored Makefile still contains the BUILD_TAG=broken perturbation."

def test_log_sanitiser_builds():
    main_go_path = "/home/user/log-sanitiser/main.go"
    assert os.path.exists(main_go_path), f"main.go missing at {main_go_path}"

    build_cmd = ["go", "build", "-o", "/tmp/log-sanitiser", "main.go"]
    result = subprocess.run(build_cmd, cwd="/home/user/log-sanitiser", capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to build main.go:\n{result.stderr}"

def test_adversarial_corpus():
    binary_path = "/tmp/log-sanitiser"
    if not os.path.exists(binary_path):
        pytest.fail("Binary not built, skipping corpus tests.")

    clean_dir = "/home/user/corpus/clean/"
    evil_dir = "/home/user/corpus/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    failed_clean = []
    failed_evil = []

    for cfile in clean_files:
        if not os.path.isfile(cfile): continue
        with open(cfile, "r") as f:
            expected_output = f.read().strip()

        result = subprocess.run([binary_path, cfile], capture_output=True, text=True)
        if result.returncode != 0:
            failed_clean.append(f"{os.path.basename(cfile)} (non-zero exit code: {result.returncode})")
            continue

        actual_output = result.stdout.strip()
        if actual_output != expected_output:
            failed_clean.append(f"{os.path.basename(cfile)} (output mismatch)")

    for efile in evil_files:
        if not os.path.isfile(efile): continue
        result = subprocess.run([binary_path, efile], capture_output=True, text=True)
        if result.returncode != 0:
            failed_evil.append(f"{os.path.basename(efile)} (non-zero exit code: {result.returncode})")
            continue

        actual_output = result.stdout.strip()
        if actual_output != "":
            failed_evil.append(f"{os.path.basename(efile)} (output not empty)")

    error_msgs = []
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: " + ", ".join(failed_evil))
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified: " + ", ".join(failed_clean))

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))