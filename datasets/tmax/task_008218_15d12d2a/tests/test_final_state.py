# test_final_state.py

import os
import stat
import gzip

def test_script_exists_and_executable():
    script_path = "/home/user/archive_errors.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable by the owner."

def test_script_uses_flock():
    script_path = "/home/user/archive_errors.sh"
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "flock -s" in content or "flock --shared" in content, \
        "Script does not use 'flock -s' or 'flock --shared' as required to acquire a shared lock."

def test_archive_exists():
    archive_path = "/home/user/archive/recent_errors.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

def test_archive_contents():
    archive_path = "/home/user/archive/recent_errors.gz"
    assert os.path.isfile(archive_path), f"Cannot verify contents, {archive_path} is missing."

    expected_content = """[ERROR]
Database connection timeout
Retry count: 3
[END ERROR]
[ERROR]
NullPointerException
at com.example.Main.main(Main.java:15)
[END ERROR]
[ERROR]
Disk space low
Volume: /dev/sda1
[END ERROR]"""

    try:
        with gzip.open(archive_path, "rt", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        assert False, f"Failed to read {archive_path} as a gzip file: {e}"

    assert content.strip() == expected_content.strip(), \
        "The extracted error blocks in the gzip file do not match the expected output or are not in alphabetical order."