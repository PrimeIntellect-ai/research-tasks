# test_final_state.py

import os
import subprocess
import shutil
import tarfile
import zipfile
import io
import pytest

def test_safe_extractor_metric():
    script_path = "/home/user/safe_extractor.py"
    assert os.path.exists(script_path), f"Agent script not found at {script_path}"

    hidden_archive = "/tmp/hidden_eval_backup.tar.gz"
    eval_out_dir = "/tmp/eval_restored_data"

    # Create hidden test archive
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("safe.txt", b"safe")
        zf.writestr("../../../tmp/eval_restored_data_evil/evil.txt", b"evil1")
        zf.writestr("/absolute/path/evil2.txt", b"evil2")

    zip_buffer.seek(0)
    with tarfile.open(hidden_archive, "w:gz") as tf:
        tarinfo = tarfile.TarInfo("nested.zip")
        tarinfo.size = len(zip_buffer.getvalue())
        tf.addfile(tarinfo, zip_buffer)

    if os.path.exists(eval_out_dir):
        shutil.rmtree(eval_out_dir)
    os.makedirs(eval_out_dir)

    # Run the agent's script
    cmd = ["python3", script_path, hidden_archive, eval_out_dir]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Agent script failed with error: {result.stderr}"

    # Calculate accuracy
    correct_actions = 0
    total_files = 3

    if os.path.exists(os.path.join(eval_out_dir, "safe.txt")):
        correct_actions += 1

    if not os.path.exists("/tmp/eval_restored_data_evil/evil.txt"):
        correct_actions += 1

    if not os.path.exists("/absolute/path/evil2.txt"):
        correct_actions += 1

    accuracy = correct_actions / total_files

    # Clean up evil files if they were accidentally extracted
    if os.path.exists("/tmp/eval_restored_data_evil/evil.txt"):
        os.remove("/tmp/eval_restored_data_evil/evil.txt")
    if os.path.exists("/absolute/path/evil2.txt"):
        os.remove("/absolute/path/evil2.txt")

    assert accuracy >= 1.0, f"Extraction Security Accuracy: {accuracy} < 1.0 threshold. Script did not correctly handle all files."

def test_restored_data_directory():
    # Check if the agent actually executed the script on the sample backup
    target_dir = "/home/user/restored_data"
    assert os.path.isdir(target_dir), f"Target directory {target_dir} was not created. Did you run the script against the sample backup?"

    # Just check that it's not empty
    files = os.listdir(target_dir)
    assert len(files) > 0, f"Target directory {target_dir} is empty."