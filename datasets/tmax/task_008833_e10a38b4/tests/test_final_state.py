# test_final_state.py
import os
import tarfile

def test_anomalies_csv_contents():
    csv_path = "/home/user/data/anomalies.csv"
    assert os.path.isfile(csv_path), f"Expected file {csv_path} does not exist."

    expected_content = [
        "station,temp",
        "ST-A1,43.0",
        "ST-A1,41.2",
        "ST-A2,40.0",
        "ST-B1,42.5",
        "ST-C1,45.1",
        "ST-C2,40.5"
    ]

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_content, f"Content of {csv_path} does not match expected output. Got: {lines}"

def test_anomalies_tar_gz():
    tar_path = "/home/user/data/anomalies.tar.gz"
    assert os.path.isfile(tar_path), f"Expected file {tar_path} does not exist."
    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar archive."

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        assert names == ["anomalies.csv"], f"Archive should contain exactly 'anomalies.csv' (no nested directories). Got: {names}"