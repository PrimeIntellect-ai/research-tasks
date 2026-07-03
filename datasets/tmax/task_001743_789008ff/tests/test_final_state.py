# test_final_state.py
import os
import glob
import subprocess

def test_filter_script_validation():
    script_path = '/home/user/filter.sh'
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    clean_dir = '/app/corpus/clean'
    evil_dir = '/app/corpus/evil'

    clean_tars = glob.glob(os.path.join(clean_dir, '*.tar'))
    evil_tars = glob.glob(os.path.join(evil_dir, '*.tar'))

    assert len(clean_tars) > 0, f"No clean tar files found in {clean_dir}."
    assert len(evil_tars) > 0, f"No evil tar files found in {evil_dir}."

    clean_failed = []
    evil_failed = []

    # Test clean corpus (should exit 0)
    for tar in clean_tars:
        result = subprocess.run(['bash', script_path, tar], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(tar))

    # Test evil corpus (should exit non-zero)
    for tar in evil_tars:
        result = subprocess.run(['bash', script_path, tar], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(tar))

    error_msg = []
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} of {len(evil_tars)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} of {len(clean_tars)} clean rejected: {', '.join(clean_failed)}")

    assert not evil_failed and not clean_failed, " | ".join(error_msg)