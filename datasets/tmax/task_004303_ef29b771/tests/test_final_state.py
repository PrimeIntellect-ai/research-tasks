# test_final_state.py

import os
import zipfile

def test_organize_py_exists_and_contains_flock():
    script_path = "/home/user/organize.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "fcntl.flock" in content, f"The script {script_path} does not contain 'fcntl.flock'."
    assert "fcntl.LOCK_EX" in content, f"The script {script_path} does not contain 'fcntl.LOCK_EX'."

def test_clean_assets_zip():
    zip_path = "/home/user/clean_assets.zip"
    assert os.path.exists(zip_path), f"The archive {zip_path} does not exist."
    assert os.path.isfile(zip_path), f"{zip_path} is not a file."
    assert zipfile.is_zipfile(zip_path), f"{zip_path} is not a valid ZIP file."

    expected_files = {"asset_config1.yaml", "asset_settings.yaml", "asset_root_level.yaml"}

    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()

        # Check that files are at the root (no directory separators)
        for name in namelist:
            assert "/" not in name and "\\" not in name, f"File {name} in the ZIP archive is not at the root level."

        actual_files = set(namelist)
        assert actual_files == expected_files, f"ZIP contents mismatch. Expected {expected_files}, got {actual_files}."

        # Check content of asset_config1.yaml
        config1_content = zf.read("asset_config1.yaml").decode("utf-8")
        assert "processed: true" in config1_content or "processed: True" in config1_content, "asset_config1.yaml does not contain 'processed: true'."
        assert "ServiceA" in config1_content, "asset_config1.yaml is missing original data."

def test_processing_directory_state():
    processing_dir = "/home/user/processing"
    assert os.path.exists(processing_dir), f"The directory {processing_dir} does not exist."
    assert os.path.isdir(processing_dir), f"{processing_dir} is not a directory."

    json_files = []
    yaml_files = []

    for root, dirs, files in os.walk(processing_dir):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
            elif file.endswith(".yaml"):
                yaml_files.append(os.path.join(root, file))

    assert len(json_files) == 0, f"Found leftover .json files in {processing_dir}: {json_files}"

    expected_yaml_names = {"asset_config1.yaml", "asset_settings.yaml", "asset_root_level.yaml"}
    actual_yaml_names = {os.path.basename(p) for p in yaml_files}
    assert expected_yaml_names.issubset(actual_yaml_names), f"Missing expected .yaml files in {processing_dir}. Expected {expected_yaml_names}, got {actual_yaml_names}."