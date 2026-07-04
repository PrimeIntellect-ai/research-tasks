# test_final_state.py

import os
import json
import subprocess

def test_rust_core_compiles():
    cargo_toml = "/home/user/release_prep/core/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Cargo.toml missing at {cargo_toml}"

    result = subprocess.run(
        ["cargo", "check", "--manifest-path", cargo_toml],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Rust project failed to compile:\n{result.stderr}"

def test_deploy_report_exists_and_matches():
    report_path = "/home/user/deploy_report.json"
    assert os.path.isfile(report_path), f"Deploy report missing at {report_path}"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Deploy report at {report_path} is not valid JSON"

    assert report.get("rust_compiled") is True, "Expected 'rust_compiled' to be true"
    assert report.get("rules_evaluated_to") is True, "Expected 'rules_evaluated_to' to be true"
    assert report.get("applied_patches") == ["01-update-db.diff", "02-update-cache.diff"], "Expected 'applied_patches' to match the specific list"
    assert report.get("final_patch_created") is True, "Expected 'final_patch_created' to be true"

def test_consolidated_patch_created():
    patch_path = "/home/user/release_prep/consolidated.patch"
    assert os.path.isfile(patch_path), f"Consolidated patch missing at {patch_path}"

def test_settings_ini_patched():
    settings_path = "/home/user/release_prep/config/settings.ini"
    assert os.path.isfile(settings_path), f"Settings file missing at {settings_path}"

    with open(settings_path, "r") as f:
        content = f.read()

    assert "host = db.internal" in content, "settings.ini not patched correctly: missing 'host = db.internal'"
    assert "enabled = true" in content, "settings.ini not patched correctly: missing 'enabled = true'"
    assert "host = localhost" not in content, "settings.ini still contains 'host = localhost'"
    assert "enabled = false" not in content, "settings.ini still contains 'enabled = false'"

def test_test_deploy_py_exists():
    test_path = "/home/user/release_prep/test_deploy.py"
    assert os.path.isfile(test_path), f"Test file missing at {test_path}"

    with open(test_path, "r") as f:
        content = f.read()
        assert "def test_" in content or "class Test" in content, "Test file does not appear to contain any tests"