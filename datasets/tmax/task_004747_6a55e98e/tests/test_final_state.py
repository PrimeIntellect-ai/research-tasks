# test_final_state.py

import os
import json
import subprocess
import pytest

def test_make_test_succeeds():
    """Verify that 'make test' runs successfully in /home/user/app/."""
    app_dir = "/home/user/app"
    assert os.path.isdir(app_dir), f"Directory {app_dir} does not exist."

    result = subprocess.run(
        ["make", "test"],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"'make test' failed.\nstdout: {result.stdout}\nstderr: {result.stderr}"

def test_resolution_json_exists_and_valid():
    """Verify that resolution.json exists and is valid JSON."""
    res_path = "/home/user/app/resolution.json"
    assert os.path.isfile(res_path), f"File {res_path} is missing."

    with open(res_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"{res_path} is not valid JSON: {e}")

    assert isinstance(data, dict), "resolution.json should contain a JSON object."
    assert "magic_hex" in data, "Key 'magic_hex' missing from resolution.json."
    assert "original_encoding" in data, "Key 'original_encoding' missing from resolution.json."

def test_resolution_json_values():
    """Verify the values in resolution.json."""
    res_path = "/home/user/app/resolution.json"
    with open(res_path, "r") as f:
        data = json.load(f)

    magic_hex = str(data.get("magic_hex", "")).lower().strip()
    assert magic_hex == "deadc0de", f"Expected magic_hex to be 'deadc0de', got '{magic_hex}'"

    encoding = str(data.get("original_encoding", "")).lower().replace("-", "").replace("_", "").replace(" ", "")
    assert "utf16" in encoding, f"Expected original_encoding to indicate utf-16le, got '{data.get('original_encoding')}'"
    if "le" not in encoding and encoding != "utf16":
        # It's okay if they just say utf-16, but if they add something else, ensure it's correct
        pass

def test_makefile_updated():
    """Verify that the Makefile was updated to use fixed.dat."""
    makefile_path = "/home/user/app/Makefile"
    assert os.path.isfile(makefile_path), f"File {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "data/fixed.dat" in content, "Makefile does not reference 'data/fixed.dat'."
    assert "data/raw.dat" not in content, "Makefile should no longer reference 'data/raw.dat'."

def test_fixed_dat_exists():
    """Verify that fixed.dat was created."""
    fixed_path = "/home/user/app/data/fixed.dat"
    assert os.path.isfile(fixed_path), f"File {fixed_path} is missing."