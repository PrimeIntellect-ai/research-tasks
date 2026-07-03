# test_final_state.py
import os

def test_build_success_log():
    log_path = '/home/user/project/build_success.log'
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. Did you redirect the output of build.sh?"

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == "BUILD SUCCESSFUL", f"Expected '{log_path}' to contain exactly 'BUILD SUCCESSFUL', but found '{content}'."

def test_cleaned_asset_file():
    asset_path = '/home/user/project/assets/config_data.bin'
    assert os.path.isfile(asset_path), f"The file {asset_path} does not exist."

    with open(asset_path, 'rb') as f:
        content = f.read()

    assert content == b"VALID_ASSET_123", f"Expected '{asset_path}' to contain exactly 'VALID_ASSET_123', but found {content!r}."