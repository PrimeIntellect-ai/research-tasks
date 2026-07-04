# test_final_state.py
import os
import tarfile

def test_merger_c_exists():
    assert os.path.isfile('/home/user/merger.c'), "The C program /home/user/merger.c was not found."

def test_assembled_archive_exists_and_valid():
    archive_path = '/home/user/staging/assembled.tar.gz'
    assert os.path.isfile(archive_path), f"The assembled archive {archive_path} was not found."

    # Check if it's a valid tar.gz file
    try:
        assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."
        with tarfile.open(archive_path, 'r:gz') as tar:
            names = tar.getnames()
            assert 'secret_key.txt' in names, "secret_key.txt not found in the assembled archive."
    except Exception as e:
        assert False, f"Failed to open or validate {archive_path}: {e}"

def test_extracted_secret_key():
    secret_path = '/home/user/release/secret_key.txt'
    assert os.path.isfile(secret_path), f"The extracted file {secret_path} was not found."

    with open(secret_path, 'r') as f:
        content = f.read().strip()

    assert content == "ARTIFACT_VERIFIED_77392", f"Incorrect content in {secret_path}. Expected 'ARTIFACT_VERIFIED_77392', got '{content}'."