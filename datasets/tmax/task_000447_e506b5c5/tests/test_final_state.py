# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/cfg_manager"
RAW_DIR = os.path.join(BASE_DIR, "raw")
EXTRACTED_DIR = os.path.join(BASE_DIR, "extracted")
FINAL_CONFIG = os.path.join(BASE_DIR, "final_config.txt")
EXTRACTOR_C = os.path.join(BASE_DIR, "extractor.c")

def test_step1_renaming():
    """Verify that the raw files were renamed from .dat to .cpk."""
    assert os.path.isdir(RAW_DIR), f"Raw directory {RAW_DIR} is missing."

    dat_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".dat")]
    assert not dat_files, f"Found .dat files that should have been renamed: {dat_files}"

    cpk_files = [f for f in os.listdir(RAW_DIR) if f.endswith(".cpk")]
    assert "archive_01.cpk" in cpk_files, "archive_01.cpk is missing."
    assert "archive_02.cpk" in cpk_files, "archive_02.cpk is missing."

def test_step2_c_program_exists():
    """Verify that the C program was created."""
    assert os.path.isfile(EXTRACTOR_C), f"C program {EXTRACTOR_C} is missing."

def test_step3_extracted_files():
    """Verify that the files were extracted and updated correctly."""
    assert os.path.isdir(EXTRACTED_DIR), f"Extracted directory {EXTRACTED_DIR} is missing."

    expected_files = {"alpha.conf", "beta.conf", "gamma.conf", "delta.conf"}
    actual_files = set(os.listdir(EXTRACTED_DIR))

    assert expected_files.issubset(actual_files), f"Missing extracted files. Expected {expected_files}, found {actual_files}"

    # Check that replacement happened in one of the files
    alpha_path = os.path.join(EXTRACTED_DIR, "alpha.conf")
    with open(alpha_path, "r") as f:
        content = f.read()
        assert "db_host=db-cluster.aws.internal" in content, f"db_host was not updated in {alpha_path}"
        assert "legacy-db.local" not in content, f"legacy-db.local was not completely replaced in {alpha_path}"

def test_step4_final_config_content():
    """Verify the final merged configuration file."""
    assert os.path.isfile(FINAL_CONFIG), f"Final configuration file {FINAL_CONFIG} is missing."

    expected_content = (
        "=== alpha.conf ===\n"
        "loglevel=info\n"
        "db_host=db-cluster.aws.internal\n"
        "max_conns=100\n"
        "=== beta.conf ===\n"
        "timeout=30\n"
        "db_host=db-cluster.aws.internal\n"
        "=== delta.conf ===\n"
        "cache_size=1024\n"
        "db_host=db-cluster.aws.internal\n"
        "=== gamma.conf ===\n"
        "enable_feature_x=true\n"
    )

    with open(FINAL_CONFIG, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        "The contents of final_config.txt do not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )