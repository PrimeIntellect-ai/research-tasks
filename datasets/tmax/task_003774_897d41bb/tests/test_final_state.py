# test_final_state.py
import os
import subprocess
import glob

def test_flash_detector_output():
    output_file = '/home/user/flash_count.txt'
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist. Did you run the flash detector script?"

    with open(output_file, 'r') as f:
        content = f.read().strip()

    assert content == '5', f"Expected flash count to be 5, but got '{content}'."

def test_sanitizer_adversarial_corpus():
    sanitizer_script = '/home/user/sanitizer.py'
    assert os.path.isfile(sanitizer_script), f"Sanitizer script {sanitizer_script} does not exist."

    clean_dir = '/app/corpus/clean'
    evil_dir = '/app/corpus/evil'

    clean_files = glob.glob(os.path.join(clean_dir, '*'))
    evil_files = glob.glob(os.path.join(evil_dir, '*'))

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    clean_failures = []
    for clean_file in clean_files:
        result = subprocess.run(['python3', sanitizer_script, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(clean_file))

    evil_failures = []
    for evil_file in evil_files:
        result = subprocess.run(['python3', sanitizer_script, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(evil_file))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_messages:
        assert False, " | ".join(error_messages)