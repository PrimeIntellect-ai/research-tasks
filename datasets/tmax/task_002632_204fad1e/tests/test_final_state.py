# test_final_state.py

import os
import subprocess
import tarfile

def test_zip_slip_prevented():
    assert not os.path.exists('/tmp/hacked.txt'), "Zip slip vulnerability was not prevented; /tmp/hacked.txt exists."

def test_settings_extracted_correctly():
    settings_path = '/home/user/update_extracted/settings.conf'
    assert os.path.exists(settings_path), f"{settings_path} does not exist."
    with open(settings_path, 'r') as f:
        content = f.read()
    assert 'TargetDirectory=/app/data_dir' in content, f"Expected 'TargetDirectory=/app/data_dir' in {settings_path}, but got: {content}"

def test_incremental_backup_created():
    backup_path = '/home/user/incremental_backup.tar.gz'
    assert os.path.exists(backup_path), f"{backup_path} does not exist."
    assert tarfile.is_tarfile(backup_path), f"{backup_path} is not a valid tar file."

    # Check that file2.txt is in the incremental backup
    with tarfile.open(backup_path, 'r:gz') as tar:
        names = tar.getnames()
        # The path in tar might be data_dir/file2.txt or app/data_dir/file2.txt
        assert any('file2.txt' in name for name in names), "Incremental backup does not contain the new file 'file2.txt'."

def test_backup_log_created():
    log_path = '/home/user/backup_files.log'
    assert os.path.exists(log_path), f"{log_path} does not exist."
    with open(log_path, 'r') as f:
        content = f.read()
    assert len(content.strip()) > 0, f"{log_path} is empty."

def test_audio_compression_metric():
    ogg_path = '/home/user/compressed_memo.ogg'
    assert os.path.exists(ogg_path), f"Compressed audio file {ogg_path} does not exist."

    size = os.path.getsize(ogg_path)

    try:
        subprocess.run(["ffprobe", "-v", "error", ogg_path], check=True, capture_output=True)
        valid = True
    except subprocess.CalledProcessError as e:
        valid = False
        assert False, f"ffprobe failed to validate {ogg_path} as a valid media file. Error: {e.stderr.decode()}"

    assert valid, f"{ogg_path} is not a valid decodable file."
    assert size <= 15000, f"File size of {ogg_path} is {size} bytes, which exceeds the threshold of 15000 bytes."