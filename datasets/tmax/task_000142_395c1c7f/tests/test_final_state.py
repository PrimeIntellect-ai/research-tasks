# test_final_state.py

import os
import re

def test_mc_volume_script_exists():
    script_path = "/home/user/mc_volume.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_volume_estimate_output():
    output_path = "/home/user/volume_estimate.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    match = re.search(r'Estimated Volume:\s*([0-9.]+)', content)
    assert match is not None, "Format error: Could not find 'Estimated Volume: <value>' in the output file."

    vol = float(match.group(1))
    assert 44.0 <= vol <= 47.0, f"Value out of bounds: {vol}. Expected between 44.0 and 47.0."