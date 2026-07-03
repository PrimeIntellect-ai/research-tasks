# test_final_state.py
import os
import json
import tarfile
import xml.etree.ElementTree as ET

def test_rotated_configs_tarball():
    tarball_path = "/home/user/rotated_configs.tar.gz"
    assert os.path.exists(tarball_path), f"Tarball {tarball_path} does not exist."
    assert tarfile.is_tarfile(tarball_path), f"{tarball_path} is not a valid tar file."

    # Compute expected files based on the current state of /home/user/configs
    configs_dir = "/home/user/configs"
    expected_files = {}

    for app_name in os.listdir(configs_dir):
        app_dir = os.path.join(configs_dir, app_name)
        if not os.path.isdir(app_dir):
            continue

        metadata_path = os.path.join(app_dir, "metadata.json")
        config_path = os.path.join(app_dir, "config.xml")

        if not os.path.exists(metadata_path) or not os.path.exists(config_path):
            continue

        with open(metadata_path, 'r') as f:
            try:
                metadata = json.load(f)
            except json.JSONDecodeError:
                continue

        if metadata.get("status") == "rotating":
            try:
                tree = ET.parse(config_path)
                version_text = tree.getroot().findtext("version")
                if version_text and int(version_text) > 1:
                    expected_filename = f"{app_name}_v{version_text}.xml"
                    with open(config_path, 'rb') as cf:
                        expected_files[expected_filename] = cf.read()
            except Exception:
                pass

    # Inspect tarball
    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            members = tar.getmembers()

            # The files should be placed at the root of the archive
            member_names = [m.name.lstrip('./') for m in members if m.isfile()]

            assert set(member_names) == set(expected_files.keys()), \
                f"Expected files in tarball: {sorted(list(expected_files.keys()))}, but found: {sorted(member_names)}"

            for member in members:
                if not member.isfile():
                    continue

                normalized_name = member.name.lstrip('./')
                f = tar.extractfile(member)
                assert f is not None, f"Could not extract {member.name} from tarball."
                content = f.read()
                assert content == expected_files[normalized_name], \
                    f"Content of {member.name} in tarball does not match the original config.xml."
    except tarfile.ReadError:
        assert False, f"{tarball_path} is not a valid gzip-compressed tar archive."