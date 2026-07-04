# test_final_state.py
import os
import tarfile
import tempfile

def test_old_records_deleted():
    assert not os.path.exists("/home/user/old_records"), "/home/user/old_records directory should be deleted."

def test_summary_txt():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"{summary_path} does not exist."
    with open(summary_path, 'r') as f:
        content = f.read().strip()
    assert content == "8", f"Expected summary.txt to contain '8', but found '{content}'."

def test_archive_exists_and_valid():
    archive_path = "/home/user/old_records_archive.tar.gz"
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."

def find_file(root_dir, filename):
    for dirpath, _, filenames in os.walk(root_dir):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None

def test_archive_contents():
    archive_path = "/home/user/old_records_archive.tar.gz"
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."

    with tarfile.open(archive_path, "r:gz") as tar:
        with tempfile.TemporaryDirectory() as tmpdir:
            tar.extractall(path=tmpdir)

            app_log = find_file(tmpdir, "app.log")
            old_data = find_file(tmpdir, "old_data.txt")
            ignore_me = find_file(tmpdir, "ignore_me.csv")
            root_log = find_file(tmpdir, "root_level.log")

            assert app_log is not None, "app.log missing in archive."
            assert old_data is not None, "old_data.txt missing in archive."
            assert ignore_me is not None, "ignore_me.csv missing in archive."
            assert root_log is not None, "root_level.log missing in archive."

            with open(app_log, 'r') as f:
                content = f.read()
                assert "[VERBOSE-DUMP]" not in content, "app.log still contains [VERBOSE-DUMP] lines."
                assert "[INFO] Application started" in content, "app.log is missing expected valid lines."
                assert "[WARN] Connection timeout" in content, "app.log is missing expected valid lines."

            with open(old_data, 'r') as f:
                content = f.read()
                assert "[VERBOSE-DUMP]" not in content, "old_data.txt still contains [VERBOSE-DUMP] lines."
                assert "Data line 1" in content, "old_data.txt is missing expected valid lines."
                assert "Data line 2" in content, "old_data.txt is missing expected valid lines."

            with open(root_log, 'r') as f:
                content = f.read()
                assert "[VERBOSE-DUMP]" not in content, "root_level.log still contains [VERBOSE-DUMP] lines."
                assert "[INFO] Root initialized" in content, "root_level.log is missing expected valid lines."

            with open(ignore_me, 'r') as f:
                content = f.read()
                assert "[VERBOSE-DUMP]" in content, "ignore_me.csv should NOT have been modified, but [VERBOSE-DUMP] is missing."
                assert "1,alice" in content, "ignore_me.csv is missing expected valid lines."