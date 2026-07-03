# test_final_state.py

import os
import subprocess

def test_failing_assets_txt():
    path = "/home/user/failing_assets.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"Expected exactly one line in {path}, found {len(lines)}."
    assert lines[0] == "ui background.png", f"Expected 'ui background.png' in {path}, got '{lines[0]}'."

def test_build_fixed_sh_exists_and_executable():
    path = "/home/user/project/build_fixed.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_build_fixed_sh_execution_and_output():
    out_dir = "/home/user/project/out"

    # Clear out directory first to ensure we test the script's actual output
    if os.path.isdir(out_dir):
        for f in os.listdir(out_dir):
            os.remove(os.path.join(out_dir, f))
    else:
        os.makedirs(out_dir)

    # Run the fixed script
    script_path = "/home/user/project/build_fixed.sh"
    result = subprocess.run([script_path], cwd="/home/user/project", capture_output=True, text=True)
    assert result.returncode == 0, f"build_fixed.sh failed with return code {result.returncode}.\nstdout: {result.stdout}\nstderr: {result.stderr}"

    expected_files = [
        "logo.png.out",
        "ui background.png.out",
        "icon.png.out"
    ]
    unexpected_files = [
        "hero image.jpg.out"
    ]

    # Check expected files
    for f in expected_files:
        f_path = os.path.join(out_dir, f)
        assert os.path.isfile(f_path), f"Expected output file {f_path} is missing."
        with open(f_path, "r") as out_file:
            content = out_file.read().strip()
        assert content == "COMPILED ASSET MAGIC", f"File {f_path} has incorrect content: '{content}'."

    # Check unexpected files
    for f in unexpected_files:
        f_path = os.path.join(out_dir, f)
        assert not os.path.exists(f_path), f"Unexpected output file {f_path} exists (asset should be inactive)."