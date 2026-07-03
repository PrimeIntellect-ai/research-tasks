# test_final_state.py

import os
import pytest

WORKSPACE = "/home/user/workspace"
MANIFEST = os.path.join(WORKSPACE, "manifest.txt")
MRE_SCRIPT = os.path.join(WORKSPACE, "mre_race.sh")
PROCESS_ASSETS_SH = os.path.join(WORKSPACE, "process_assets.sh")
COMPILE_SH = os.path.join(WORKSPACE, "compile.sh")

def test_mre_script_exists():
    assert os.path.isfile(MRE_SCRIPT), f"Minimal reproducible example script {MRE_SCRIPT} is missing."

def test_manifest_exists():
    assert os.path.isfile(MANIFEST), f"Manifest file {MANIFEST} is missing. Did you run build.sh?"

def test_manifest_contents_correct():
    with open(MANIFEST, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    png_count = sum(1 for line in lines if line.endswith(".png"))
    co_count = sum(1 for line in lines if line.endswith(".c.o"))

    assert png_count == 100, f"Expected exactly 100 .png entries in {MANIFEST}, but found {png_count}. The recursion or race condition might not be fully fixed."
    assert co_count == 100, f"Expected exactly 100 .c.o entries in {MANIFEST}, but found {co_count}. The race condition might not be fully fixed."
    assert len(lines) == 200, f"Expected exactly 200 valid entries in {MANIFEST}, but found {len(lines)}."

def test_scripts_modified_for_safety():
    with open(PROCESS_ASSETS_SH, "r") as f:
        process_content = f.read()

    with open(COMPILE_SH, "r") as f:
        compile_content = f.read()

    # Check that the original unsafe read-write pattern has been removed or modified
    unsafe_pattern = 'contents=$(cat /home/user/workspace/manifest.txt)\n            echo -e "${contents}\\n$f" > /home/user/workspace/manifest.txt'
    unsafe_pattern_compile = 'contents=$(cat /home/user/workspace/manifest.txt)\n        echo -e "${contents}\\n$f.o" > /home/user/workspace/manifest.txt'

    assert unsafe_pattern not in process_content, "The original race condition pattern is still present in process_assets.sh."
    assert unsafe_pattern_compile not in compile_content, "The original race condition pattern is still present in compile.sh."