# test_final_state.py

import os
import subprocess
import glob
import codecs

def test_backup_filter_script_exists():
    assert os.path.isfile('/home/user/backup_filter.py'), "backup_filter.py not found at /home/user/backup_filter.py"

def test_adversarial_corpus_filtering():
    script_path = '/home/user/backup_filter.py'
    clean_dir = '/app/corpora/clean'
    evil_dir = '/app/corpora/evil'

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for f in clean_files:
        result = subprocess.run(['python3', script_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run(['python3', script_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean files modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil files bypassed: {', '.join(evil_failures)}")

    assert not error_messages, "Adversarial corpus verification failed: " + " | ".join(error_messages)

def test_processed_backup_directory():
    processed_dir = '/home/user/processed_backup'
    assert os.path.isdir(processed_dir), f"{processed_dir} directory does not exist."

    files = os.listdir(processed_dir)
    assert len(files) > 0, f"No files found in {processed_dir}."

    for f in files:
        assert f.startswith('BKP_2024_'), f"File {f} does not have the mandatory prefix 'BKP_2024_'."
        assert ' ' not in f, f"File {f} contains spaces, which should have been replaced with underscores."

        filepath = os.path.join(processed_dir, f)

        # Check UTF-8 encoding
        try:
            with codecs.open(filepath, 'r', encoding='utf-8') as file_obj:
                content = file_obj.read()
        except UnicodeDecodeError:
            assert False, f"File {f} is not properly encoded in UTF-8."

        # Check that no malware signature is present
        assert '[MALWARE-SIGNATURE-8821]' not in content, f"File {f} contains the malware signature, it should have been deleted."