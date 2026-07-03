# test_final_state.py

import os
import pytest

def test_files_exist():
    expected_files = [
        "/home/user/compute_cov.c",
        "/home/user/compute_cov",
        "/home/user/test_reproducibility.sh",
        "/home/user/split1.csv",
        "/home/user/split2.csv",
        "/home/user/cov1.txt",
        "/home/user/cov2.txt"
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected file {file_path} does not exist."

def test_sh_executable():
    sh_path = "/home/user/test_reproducibility.sh"
    assert os.access(sh_path, os.X_OK), f"Script {sh_path} is not executable."

def test_cov_outputs():
    cov1_path = "/home/user/cov1.txt"
    cov2_path = "/home/user/cov2.txt"

    expected_cov1 = [
        "2.4570 2.2380 2.2130",
        "2.2380 2.2230 2.0620",
        "2.2130 2.0620 2.0570"
    ]

    expected_cov2 = [
        "2.5750 2.3600 2.6500",
        "2.3600 2.2670 2.4930",
        "2.6500 2.4930 2.7670"
    ]

    with open(cov1_path, 'r') as f:
        cov1_lines = [line.strip() for line in f if line.strip()]

    assert cov1_lines == expected_cov1, f"Content of {cov1_path} does not match expected output. Got: {cov1_lines}"

    with open(cov2_path, 'r') as f:
        cov2_lines = [line.strip() for line in f if line.strip()]

    assert cov2_lines == expected_cov2, f"Content of {cov2_path} does not match expected output. Got: {cov2_lines}"