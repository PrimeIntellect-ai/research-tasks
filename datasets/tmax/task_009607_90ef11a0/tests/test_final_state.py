# test_final_state.py

import os
import tarfile
import stat

def test_monitor_compiled_and_executable():
    """Verify that the compiled monitor executable exists and is executable."""
    executable_path = "/home/user/app/monitor"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    st = os.stat(executable_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Executable {executable_path} is not executable."

def test_health_log_created_and_contains_status():
    """Verify that the health.log is created in the correct location and contains a status."""
    log_path = "/home/user/app/health.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "STATUS:" in content, f"Log file {log_path} does not contain the expected 'STATUS:' string."

def test_backup_archive_created_and_valid():
    """Verify that the backup archive is created in the correct location and is a valid tarball."""
    archive_path = "/home/user/backup/health_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Backup archive {archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # The tarball should contain the log file. It could be stored with absolute or relative path,
        # but it must contain health.log in the name.
        assert any("health.log" in name for name in names), "The backup archive does not contain 'health.log'."

def test_monitor_c_uses_absolute_paths():
    """Verify that monitor.c has been updated to use absolute paths."""
    src_file = "/home/user/src/monitor.c"
    assert os.path.isfile(src_file), f"Source code file {src_file} is missing."

    with open(src_file, "r") as f:
        content = f.read()

    assert "/home/user/app/health.log" in content, "The absolute path '/home/user/app/health.log' was not found in monitor.c"
    assert "/home/user/backup/health_backup.tar.gz" in content, "The absolute path '/home/user/backup/health_backup.tar.gz' was not found in monitor.c"