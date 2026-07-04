# test_final_state.py

import os
import sys
import glob
import pytest

def test_validator_adversarial_corpus():
    """
    Tests the validate_backup function against the evil and clean corpora.
    Ensures 100% of evil backups are rejected and 100% of clean backups are accepted.
    """
    validator_path = "/home/user/backup_pipeline"
    if validator_path not in sys.path:
        sys.path.insert(0, validator_path)

    try:
        from validator import validate_backup
    except ImportError as e:
        pytest.fail(f"Could not import validate_backup from /home/user/backup_pipeline/validator.py: {e}")

    evil_dir = "/home/user/corpora/evil"
    clean_dir = "/home/user/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.tar.gz"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.tar.gz"))

    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"

    evil_bypassed = []
    for f in evil_files:
        try:
            result = validate_backup(f)
            if result is not False:
                evil_bypassed.append(os.path.basename(f))
        except Exception as e:
            # If the validator raises an exception instead of returning False, it's considered a failure to handle it gracefully.
            evil_bypassed.append(f"{os.path.basename(f)} (crashed: {e})")

    clean_rejected = []
    for f in clean_files:
        try:
            result = validate_backup(f)
            if result is not True:
                clean_rejected.append(os.path.basename(f))
        except Exception as e:
            clean_rejected.append(f"{os.path.basename(f)} (crashed: {e})")

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_rejected)}")

    if errors:
        pytest.fail(" | ".join(errors))