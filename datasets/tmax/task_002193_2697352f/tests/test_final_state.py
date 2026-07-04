# test_final_state.py
import os
import subprocess
import filecmp
import shutil

def test_archiver_and_extractor():
    archive_script = "/home/user/archive.py"
    extract_script = "/home/user/extract.py"

    assert os.path.exists(archive_script), f"{archive_script} does not exist"
    assert os.path.exists(extract_script), f"{extract_script} does not exist"

    configs_dir = "/home/user/configs"
    archive_file = "/home/user/archive.bin"
    restored_dir = "/home/user/restored"

    if os.path.exists(archive_file):
        os.remove(archive_file)
    if os.path.exists(restored_dir):
        shutil.rmtree(restored_dir)

    os.makedirs(restored_dir, exist_ok=True)

    # 1. Run archiver
    try:
        subprocess.run(
            ["python3", archive_script, configs_dir, archive_file],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        assert False, f"archive.py failed with error:\n{e.stderr}"

    assert os.path.exists(archive_file), f"Archive file {archive_file} was not created."

    # 2. Run extractor
    try:
        subprocess.run(
            ["python3", extract_script, archive_file, restored_dir],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        assert False, f"extract.py failed with error:\n{e.stderr}"

    # 3. Verify exact match
    orig_files = sorted(os.listdir(configs_dir))
    restored_files = sorted(os.listdir(restored_dir))
    assert orig_files == restored_files, "Restored file list does not match original."

    for f in orig_files:
        orig_path = os.path.join(configs_dir, f)
        rest_path = os.path.join(restored_dir, f)
        assert filecmp.cmp(orig_path, rest_path, shallow=False), f"Restored file {f} differs from original."

    # 4. Compute metric
    archive_size = os.path.getsize(archive_file)
    assert archive_size < 2000000, f"Archive size is {archive_size} bytes, which is not less than the 2000000 bytes threshold."