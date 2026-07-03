# test_final_state.py
import os
import tarfile
import tempfile
import subprocess

def test_normalized_configs_archive_exists():
    archive_path = "/home/user/normalized_configs.tar.gz"
    assert os.path.exists(archive_path), f"Missing final archive: {archive_path}"
    assert os.path.isfile(archive_path), f"Path is not a file: {archive_path}"
    assert tarfile.is_tarfile(archive_path), f"File is not a valid tar archive: {archive_path}"

def test_normalized_configs_contents_and_manifest():
    archive_path = "/home/user/normalized_configs.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."

    expected_files = {
        "prod_v1.2.4_db_settings.json",
        "staging_v2.0.0_api_limits.json",
        "dev_v3.1.0_feature_flags.csv",
        "manifest.sha256"
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        extracted_files = set(os.listdir(tmpdir))

        # Check if expected files are present
        for expected_file in expected_files:
            assert expected_file in extracted_files, f"Expected file '{expected_file}' not found in the archive."

        # Verify the manifest
        manifest_path = os.path.join(tmpdir, "manifest.sha256")
        assert os.path.exists(manifest_path), "manifest.sha256 is missing."

        # Run sha256sum -c manifest.sha256
        result = subprocess.run(
            ["sha256sum", "-c", "manifest.sha256"],
            cwd=tmpdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        assert result.returncode == 0, f"sha256sum verification failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"