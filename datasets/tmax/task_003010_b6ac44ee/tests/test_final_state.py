# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/build_project"

def test_patch_applied():
    """Test that the patch was applied to core.sh."""
    core_sh = os.path.join(BASE_DIR, "src", "core.sh")
    assert os.path.isfile(core_sh), f"{core_sh} does not exist."

    with open(core_sh, "r") as f:
        content = f.read()

    assert "VULN=1" not in content, "Patch was not applied: VULN=1 still found in core.sh."
    assert "VULN=0" in content, "Patch was not applied: VULN=0 not found in core.sh."

def test_build_order_in_app_sh():
    """Test that build.sh concatenates files in the correct order."""
    app_sh = os.path.join(BASE_DIR, "dist", "app.sh")
    assert os.path.isfile(app_sh), f"{app_sh} does not exist."

    with open(app_sh, "r") as f:
        content = f.read()

    assert "log_msg() {" in content, "app.sh is missing utils.sh content."
    assert "validate_input()" in content, "app.sh is missing core.sh content."
    assert "main()" in content, "app.sh is missing main.sh content."

    util_idx = content.find("log_msg() {")
    core_idx = content.find("validate_input()")
    main_idx = content.find("main()")

    assert util_idx < core_idx, "Incorrect build order: utils.sh must precede core.sh."
    assert core_idx < main_idx, "Incorrect build order: core.sh must precede main.sh."

    assert os.access(app_sh, os.X_OK), "dist/app.sh is not executable."

def test_fuzzing_report():
    """Test that report.txt exists and contains the correct string."""
    report_txt = os.path.join(BASE_DIR, "report.txt")
    assert os.path.isfile(report_txt), "report.txt was not generated."

    with open(report_txt, "r") as f:
        content = f.read().strip()

    assert content == "FUZZING SUCCESS", f"report.txt content is incorrect. Expected 'FUZZING SUCCESS', got '{content}'."

def test_resource_leak_fixed():
    """Test that running app.sh does not leave files in the cache directory."""
    app_sh = os.path.join(BASE_DIR, "dist", "app.sh")
    cache_dir = os.path.join(BASE_DIR, "cache")

    assert os.path.isfile(app_sh), f"{app_sh} does not exist."
    assert os.path.isdir(cache_dir), f"{cache_dir} does not exist."

    # Run app.sh
    result = subprocess.run([app_sh, "99999"], capture_output=True, text=True)
    assert result.returncode == 0, f"app.sh failed with exit code {result.returncode}."

    # Check cache directory
    files_in_cache = os.listdir(cache_dir)
    assert len(files_in_cache) == 0, f"Resource leak detected: cache directory is not empty. Found: {files_in_cache}"