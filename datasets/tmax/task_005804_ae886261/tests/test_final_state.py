# test_final_state.py
import os
import stat
import subprocess
import tarfile
import gzip

def test_active_path_txt():
    path = '/home/user/active_path.txt'
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == '/home/user/live_config.bin', f"Expected '/home/user/live_config.bin' in {path}, got '{content}'"

def test_safe_reader_cpp():
    path = '/home/user/safe_reader.cpp'
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, 'r') as f:
        content = f.read()
    for keyword in ['mmap', 'fcntl', 'F_SETLKW', 'F_RDLCK']:
        assert keyword in content, f"Keyword '{keyword}' not found in {path}"

def test_safe_reader_executable():
    path = '/home/user/safe_reader'
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_package_backup_sh():
    path = '/home/user/package_backup.sh'
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_backup_execution_and_artifacts():
    # Run the backup script
    script_path = '/home/user/package_backup.sh'
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed with return code {result.returncode}. stderr: {result.stderr}"

    # Verify symlink
    link_path = '/home/user/latest_backup.link'
    assert os.path.islink(link_path), f"{link_path} is not a symbolic link."
    target = os.readlink(link_path)
    assert target in ['/home/user/snapshot.tar', 'snapshot.tar'], f"{link_path} points to {target}, expected /home/user/snapshot.tar or snapshot.tar"

    # Verify tar and gzip
    tar_path = '/home/user/snapshot.tar'
    assert os.path.isfile(tar_path), f"{tar_path} does not exist."

    with tarfile.open(tar_path, 'r') as tar:
        members = tar.getnames()
        assert 'snapshot.gz' in members or '/home/user/snapshot.gz' in members or any(m.endswith('snapshot.gz') for m in members), "snapshot.gz not found in tar archive."

        # Extract and verify gzip content
        gz_member = next(m for m in tar.getmembers() if m.name.endswith('snapshot.gz'))
        f_gz = tar.extractfile(gz_member)
        assert f_gz is not None, "Failed to extract snapshot.gz from tar."

        # Read gzip content
        try:
            with gzip.open(f_gz, 'rb') as gz:
                content = gz.read()
        except gzip.BadGzipFile:
            pytest.fail("snapshot.gz is not a valid gzip file.")

        # Verify content format
        assert content.startswith(b'DATA_') or content.startswith(b'INIT_DATA'), "Content of snapshot.gz does not match expected format."