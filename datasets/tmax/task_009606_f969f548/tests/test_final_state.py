# test_final_state.py

import os
import tarfile
import tempfile
import pytest

TARBALL_PATH = '/home/user/curated_configs.tar.gz'
EXTRACTED_DIR = '/home/user/extracted'

def test_tarball_exists():
    assert os.path.isfile(TARBALL_PATH), f"The tarball {TARBALL_PATH} does not exist."

def test_tarball_contents():
    assert tarfile.is_tarfile(TARBALL_PATH), f"{TARBALL_PATH} is not a valid tar archive."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(TARBALL_PATH, 'r:gz') as tar:
            tar.extractall(path=tmpdir)

            extracted_base = os.path.join(tmpdir, 'extracted')
            assert os.path.isdir(extracted_base), "The tarball must contain an 'extracted/' directory at its root."

            # Check serviceA.conf
            serviceA_path = os.path.join(extracted_base, 'serviceA.conf')
            assert os.path.isfile(serviceA_path), "extracted/serviceA.conf is missing from the tarball."
            with open(serviceA_path, 'r', encoding='utf-8') as f:
                contentA = f.read()
            assert contentA == "loglevel=DEBUG\nenv=PROD", "Incorrect content in extracted/serviceA.conf"

            # Check serviceB.conf
            serviceB_path = os.path.join(extracted_base, 'serviceB.conf')
            assert os.path.isfile(serviceB_path), "extracted/serviceB.conf is missing from the tarball."
            with open(serviceB_path, 'r', encoding='utf-8') as f:
                contentB = f.read()
            assert contentB == "loglevel=INFO\nenv=STAGING", "Incorrect content in extracted/serviceB.conf"

            # Check that serviceC and serviceD were ignored
            serviceC_path = os.path.join(extracted_base, 'serviceC.conf')
            assert not os.path.exists(serviceC_path), "extracted/serviceC.conf should not exist (size < 1000)."

            serviceD_path = os.path.join(extracted_base, 'serviceD.conf')
            assert not os.path.exists(serviceD_path), "extracted/serviceD.conf should not exist (wrong extension)."

def test_extracted_directory_contents():
    assert os.path.isdir(EXTRACTED_DIR), f"The directory {EXTRACTED_DIR} does not exist."

    serviceA_path = os.path.join(EXTRACTED_DIR, 'serviceA.conf')
    assert os.path.isfile(serviceA_path), f"{serviceA_path} is missing."
    with open(serviceA_path, 'r', encoding='utf-8') as f:
        contentA = f.read()
    assert contentA == "loglevel=DEBUG\nenv=PROD", f"Incorrect content in {serviceA_path}"

    serviceB_path = os.path.join(EXTRACTED_DIR, 'serviceB.conf')
    assert os.path.isfile(serviceB_path), f"{serviceB_path} is missing."
    with open(serviceB_path, 'r', encoding='utf-8') as f:
        contentB = f.read()
    assert contentB == "loglevel=INFO\nenv=STAGING", f"Incorrect content in {serviceB_path}"

    serviceC_path = os.path.join(EXTRACTED_DIR, 'serviceC.conf')
    assert not os.path.exists(serviceC_path), f"{serviceC_path} should not exist."

    serviceD_path = os.path.join(EXTRACTED_DIR, 'serviceD.conf')
    assert not os.path.exists(serviceD_path), f"{serviceD_path} should not exist."