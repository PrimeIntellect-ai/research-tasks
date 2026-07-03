# test_final_state.py

import os
import subprocess
import pytest

def test_phase1_deduplication():
    db_dumps_dir = '/home/user/db_dumps'
    assert os.path.isdir(db_dumps_dir), f"Directory {db_dumps_dir} is missing."

    files = [os.path.join(db_dumps_dir, f) for f in os.listdir(db_dumps_dir) if os.path.isfile(os.path.join(db_dumps_dir, f))]
    assert len(files) > 0, "No files found in /home/user/db_dumps."

    content_map = {}
    for f in files:
        with open(f, 'rb') as file:
            content = file.read()
        content_map.setdefault(content, []).append(f)

    for content, flist in content_map.items():
        inodes = set(os.stat(f).st_ino for f in flist)
        assert len(inodes) == 1, f"Phase 1 Failed: Identical files do not share the same inode. Files: {flist}"

def test_phase2_chunks():
    chunks_dir = '/home/user/archive_chunks'
    assert os.path.isdir(chunks_dir), f"Phase 2 Failed: Directory {chunks_dir} is missing."

    chunks = sorted(os.listdir(chunks_dir))
    assert len(chunks) > 0, "Phase 2 Failed: No chunks found in /home/user/archive_chunks."
    for chunk in chunks:
        assert chunk.startswith("chunk_"), f"Chunk name '{chunk}' does not match the expected 'chunk_XX' format."

def test_phase3_symlink():
    symlink_path = '/home/user/latest_archive'
    assert os.path.islink(symlink_path), f"Phase 3 Failed: {symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    assert os.path.basename(os.path.normpath(target)) == 'archive_chunks', f"Phase 3 Failed: Symlink points to {target}, expected it to point to archive_chunks."

def test_phase4_decompression_script():
    py_script = '/home/user/decompress.py'
    sh_script = '/home/user/decompress.sh'

    script_to_run = None
    cmd = []
    if os.path.exists(py_script):
        script_to_run = py_script
        cmd = ['python3', py_script]
    elif os.path.exists(sh_script):
        script_to_run = sh_script
        cmd = ['bash', sh_script]

    assert script_to_run is not None, "Phase 4 Failed: Neither decompress.py nor decompress.sh was found in /home/user/."

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Phase 4 Failed: Decompression script execution failed with exit code {e.returncode}.\nStderr: {e.stderr}")

    restored_file = '/home/user/restored_log.bin'
    original_file = '/home/user/massive_log.bin'

    assert os.path.exists(restored_file), f"Phase 4 Failed: {restored_file} was not created by the script."

    with open(original_file, 'rb') as f1, open(restored_file, 'rb') as f2:
        original_data = f1.read()
        restored_data = f2.read()

    assert original_data == restored_data, "Phase 4 Failed: The contents of restored_log.bin do not perfectly match massive_log.bin."