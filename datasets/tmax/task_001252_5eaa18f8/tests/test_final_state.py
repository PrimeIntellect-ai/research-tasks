# test_final_state.py
import os
import tarfile

def test_analysis_env_exists():
    assert os.path.isdir("/home/user/analysis_env"), "Directory /home/user/analysis_env does not exist"

def test_highest_correlation_file():
    filepath = "/home/user/analysis_env/highest_correlation.txt"
    assert os.path.isfile(filepath), f"File {filepath} does not exist"
    with open(filepath, "r") as f:
        content = f.read().strip()
    assert content == "radiation,temp,0.978", f"Expected 'radiation,temp,0.978', got '{content}'"

def test_storage_archive_exists():
    assert os.path.isdir("/home/user/storage_archive"), "Directory /home/user/storage_archive does not exist"

def test_tarball_exists():
    filepath = "/home/user/storage_archive/raw_data.tar.gz"
    assert os.path.isfile(filepath), f"File {filepath} does not exist"
    assert tarfile.is_tarfile(filepath), f"File {filepath} is not a valid tar archive"
    with tarfile.open(filepath, "r:*") as tar:
        names = tar.getnames()
        assert any("sensor_A.csv" in name for name in names), "sensor_A.csv not found in tarball"
        assert any("sensor_B.csv" in name for name in names), "sensor_B.csv not found in tarball"

def test_raw_data_deleted():
    assert not os.path.exists("/home/user/raw_data"), "Directory /home/user/raw_data was not deleted"