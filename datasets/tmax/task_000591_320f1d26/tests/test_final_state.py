# test_final_state.py

import os
import glob

def get_dir_size(path):
    total = 0
    if not os.path.exists(path):
        return 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def test_archiver_script_exists():
    script_path = '/home/user/archiver.py'
    assert os.path.isfile(script_path), f"The script {script_path} was not found."

def test_original_log_removed():
    log_path = '/home/user/raw_logs/system.log'
    assert not os.path.exists(log_path), f"The original log file {log_path} was not removed."

def test_archive_directory_and_files():
    archive_dir = '/home/user/archive'
    assert os.path.isdir(archive_dir), f"The archive directory {archive_dir} does not exist."

    chunks = glob.glob(os.path.join(archive_dir, 'system.log.chunk*.gz'))
    assert len(chunks) > 0, "No compressed chunk files found in the archive directory."

def test_archive_size_metric():
    archive_dir = '/home/user/archive'
    size = get_dir_size(archive_dir)
    threshold = 1500000
    assert size <= threshold, f"Archive size {size} bytes exceeds the threshold of {threshold} bytes."