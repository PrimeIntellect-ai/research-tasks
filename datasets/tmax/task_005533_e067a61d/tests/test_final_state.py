# test_final_state.py
import os
import json
import hashlib
import tarfile

def test_extracted_configs_exist():
    base_dir = "/home/user/extracted_configs"
    assert os.path.isdir(base_dir), f"Directory {base_dir} does not exist."
    for conf in ["web.conf", "db.conf", "cache.conf"]:
        conf_path = os.path.join(base_dir, conf)
        assert os.path.isfile(conf_path), f"Extracted file {conf_path} is missing."

def test_manifest_json():
    manifest_path = "/home/user/manifest.json"
    assert os.path.isfile(manifest_path), f"{manifest_path} does not exist."

    with open(manifest_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{manifest_path} is not valid JSON."

    assert isinstance(data, list), f"JSON in {manifest_path} must be an array."
    assert len(data) == 2, f"Expected exactly 2 objects in {manifest_path}, found {len(data)}."

    entries = {item.get("link_name"): item for item in data}

    assert "active_web" in entries, "Missing 'active_web' in manifest."
    assert "active_db" in entries, "Missing 'active_db' in manifest."

    for link_name, conf_name in [("active_web", "web.conf"), ("active_db", "db.conf")]:
        target_path = f"/home/user/extracted_configs/{conf_name}"
        assert entries[link_name].get("target_path") == target_path, \
            f"Incorrect target_path for {link_name}."

        with open(target_path, 'rb') as f:
            expected_sha256 = hashlib.sha256(f.read()).hexdigest()

        assert entries[link_name].get("sha256") == expected_sha256, \
            f"Incorrect sha256 for {link_name}."

def test_update_tar_gz():
    tar_path = "/home/user/update.tar.gz"
    assert os.path.isfile(tar_path), f"{tar_path} does not exist."
    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar archive."

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()

    # Normalize paths by removing leading './' if present
    cleaned_names = [n.lstrip("./") for n in names]

    assert "manifest.json" in cleaned_names, "manifest.json is missing from the final archive."
    assert "extracted_configs/web.conf" in cleaned_names, "extracted_configs/web.conf is missing from the final archive."
    assert "extracted_configs/db.conf" in cleaned_names, "extracted_configs/db.conf is missing from the final archive."

    assert "extracted_configs/cache.conf" not in cleaned_names, "cache.conf should not be included in the final archive."
    assert "extracted_configs/missing.conf" not in cleaned_names, "missing.conf should not be included in the final archive."