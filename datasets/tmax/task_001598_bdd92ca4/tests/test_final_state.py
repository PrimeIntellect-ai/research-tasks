# test_final_state.py
import os
import subprocess
import glob

def test_libextractor_so_exists():
    path = "/app/lib/libextractor.so"
    assert os.path.isfile(path), f"Shared library missing at {path}"

def test_filter_go_exists():
    path = "/app/filter.go"
    assert os.path.isfile(path), f"Go CLI missing at {path}"

def test_adversarial_corpus():
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run(["go", "run", "filter.go", cf], cwd="/app", capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run(["go", "run", "filter.go", ef], cwd="/app", capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified (expected exit 0, got otherwise): {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed (expected exit 1, got otherwise): {', '.join(failed_evil)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_extract_image():
    res = subprocess.run(["go", "run", "filter.go", "--extract-image"], cwd="/app", capture_output=True)
    assert res.returncode == 0, f"Expected Go tool to exit with 0 when extracting image, got {res.returncode}"

    output_path = "/app/recovered_text.txt"
    assert os.path.isfile(output_path), f"Output file missing at {output_path}"

    with open(output_path, "r") as f:
        content = f.read()

    assert "INVOICE-84920-XYZ" in content, "Recovered text does not contain the expected invoice number"