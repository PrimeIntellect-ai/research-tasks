# test_final_state.py
import os

def test_renamed_binaries():
    """
    Test that binary files meeting both criteria (>100KB, <2023-01-01) were renamed,
    and those that don't were left untouched.
    """
    # Expected to be renamed
    assert os.path.exists("/home/user/repo/groupA/legacy_artifact1.bin"), "Expected legacy_artifact1.bin to exist"
    assert not os.path.exists("/home/user/repo/groupA/artifact1.bin"), "Expected artifact1.bin to have been renamed"

    assert os.path.exists("/home/user/repo/groupC/deep/legacy_module.bin"), "Expected legacy_module.bin to exist"
    assert not os.path.exists("/home/user/repo/groupC/deep/module.bin"), "Expected module.bin to have been renamed"

    # Expected to be untouched
    assert os.path.exists("/home/user/repo/groupA/artifact2.bin"), "Expected artifact2.bin to remain unchanged (fails size criteria)"
    assert not os.path.exists("/home/user/repo/groupA/legacy_artifact2.bin"), "artifact2.bin should not be renamed"

    assert os.path.exists("/home/user/repo/groupB/artifact3.bin"), "Expected artifact3.bin to remain unchanged (fails date criteria)"
    assert not os.path.exists("/home/user/repo/groupB/legacy_artifact3.bin"), "artifact3.bin should not be renamed"

def test_config_files_updated():
    """
    Test that all .conf files have 'backend: cloud-storage' instead of 'backend: legacy-storage'.
    """
    conf_files = [
        "/home/user/repo/groupA/config.conf",
        "/home/user/repo/groupB/settings.conf",
        "/home/user/repo/groupC/deep/app.conf"
    ]

    for conf_file in conf_files:
        assert os.path.exists(conf_file), f"Config file {conf_file} is missing"
        with open(conf_file, "r") as f:
            content = f.read()
            assert "backend: cloud-storage" in content, f"File {conf_file} was not updated to cloud-storage"
            assert "backend: legacy-storage" not in content, f"File {conf_file} still contains legacy-storage"

def test_txt_file_ignored():
    """
    Test that non-.conf files were ignored during the text transformation.
    """
    txt_file = "/home/user/repo/groupB/ignore.txt"
    assert os.path.exists(txt_file), f"File {txt_file} is missing"
    with open(txt_file, "r") as f:
        content = f.read()
        assert "backend: legacy-storage" in content, f"File {txt_file} should not have been modified"
        assert "backend: cloud-storage" not in content, f"File {txt_file} should not contain cloud-storage"

def test_extracted_ids_manifest():
    """
    Test that the manifest file is generated correctly, sorted, and contains only IDs from .conf files.
    """
    manifest_path = "/home/user/extracted_ids.txt"
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} was not created"

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ids = ["alpha-99", "beta-42", "delta-05"]

    assert lines == expected_ids, f"Manifest contents are incorrect or not sorted properly. Expected {expected_ids}, got {lines}"
    assert "gamma-00" not in lines, "Manifest should not contain IDs from non-.conf files"