# test_final_state.py
import os
import stat
import tarfile
import re

def test_automate_exp_exists():
    path = "/home/user/automate.exp"
    assert os.path.isfile(path), f"Expect script {path} does not exist."

def test_backup_manager_c_exists():
    path = "/home/user/backup_manager.c"
    assert os.path.isfile(path), f"C source file {path} does not exist."

def test_backup_manager_executable():
    path = "/home/user/backup_manager"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), f"File {path} is not executable."

def test_backup_tar_gz_exists_and_contents():
    path = "/home/user/backup.tar.gz"
    assert os.path.isfile(path), f"Backup archive {path} does not exist."

    try:
        with tarfile.open(path, "r:gz") as tar:
            names = tar.getnames()
            # The tar command uses -C $(dirname $src) $(basename $src), 
            # so the path inside should start with source_data
            assert any("source_data/data.txt" in name for name in names), f"Archive does not contain 'source_data/data.txt'. Found: {names}"
    except tarfile.ReadError:
        assert False, f"File {path} is not a valid gzip-compressed tar archive."

def test_monitor_log_contents():
    path = "/home/user/monitor.log"
    assert os.path.isfile(path), f"Monitor log {path} does not exist."
    with open(path, "r") as f:
        lines = f.readlines()
    assert len(lines) > 0, f"Monitor log {path} is empty."
    assert lines[-1] == "BACKUP_SUCCESS\n", f"Monitor log does not end with 'BACKUP_SUCCESS\\n'. Last line was: {repr(lines[-1])}"

def test_fstab_out_contents():
    path = "/home/user/fstab.out"
    assert os.path.isfile(path), f"fstab output file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # UUID=12345678-1234-1234-1234-123456789abc /home/user/backup_drive ext4 defaults,noatime 0 2
    pattern = r"UUID=12345678-1234-1234-1234-123456789abc\s+/home/user/backup_drive\s+ext4\s+defaults,noatime\s+0\s+2"
    assert re.search(pattern, content), f"fstab.out does not contain the correctly formatted mount entry. Content found:\n{content}"