# test_final_state.py
import os
import tarfile
import json
import hashlib
import gzip
import tempfile

def test_processed_dataset_tar_exists():
    assert os.path.isfile("/home/user/processed_dataset.tar"), "/home/user/processed_dataset.tar does not exist."

def test_original_files_untouched():
    sensor_dir = "/home/user/sensor_data"
    expected_files = ["alpha.csv.gz", "beta.csv.gz", "gamma.csv.gz"]
    for f in expected_files:
        path = os.path.join(sensor_dir, f)
        assert os.path.isfile(path), f"Original file {path} is missing or was deleted."

def test_tar_contents_and_manifest():
    tar_path = "/home/user/processed_dataset.tar"
    assert os.path.isfile(tar_path), "Tar file missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(path=tmpdir)

        extracted_files = os.listdir(tmpdir)

        expected_csvs = ["alpha.csv", "beta.csv", "gamma.csv"]
        for f in expected_csvs:
            assert f in extracted_files, f"{f} is missing from the tar archive."

        assert "manifest.json" in extracted_files, "manifest.json is missing from the tar archive."

        # Verify JSON
        manifest_path = os.path.join(tmpdir, "manifest.json")
        with open(manifest_path, "r") as f:
            try:
                manifest = json.load(f)
            except json.JSONDecodeError:
                assert False, "manifest.json is not valid JSON."

        assert isinstance(manifest, dict), "manifest.json must contain a JSON object."

        sensor_dir = "/home/user/sensor_data"
        for csv_file in expected_csvs:
            assert csv_file in manifest, f"{csv_file} is missing from manifest.json."

            # Read extracted file and compute hash
            extracted_csv_path = os.path.join(tmpdir, csv_file)
            with open(extracted_csv_path, "rb") as f:
                extracted_data = f.read()

            actual_hash = hashlib.sha256(extracted_data).hexdigest()
            assert manifest[csv_file] == actual_hash, f"Hash mismatch in manifest for {csv_file}. Expected {actual_hash}, got {manifest[csv_file]}."

            # Compare with original uncompressed data
            gz_file = csv_file + ".gz"
            gz_path = os.path.join(sensor_dir, gz_file)
            assert os.path.isfile(gz_path), f"Original {gz_path} missing."

            with gzip.open(gz_path, "rb") as f:
                original_uncompressed_data = f.read()

            assert extracted_data == original_uncompressed_data, f"Data in {csv_file} does not match the original uncompressed data."