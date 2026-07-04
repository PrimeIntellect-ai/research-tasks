# test_final_state.py

import os

def test_analyze_script_exists():
    """Verify that the analyze.py script exists."""
    script_path = '/home/user/analyze.py'
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_top_sv_output():
    """Verify that top_sv.txt contains the correct largest singular value."""
    output_path = '/home/user/top_sv.txt'
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content == "3.22", f"Expected top_sv.txt to contain '3.22', but found '{content}'."

def test_profile_output():
    """Verify that profile.txt contains the output of /usr/bin/time -v."""
    profile_path = '/home/user/profile.txt'
    assert os.path.exists(profile_path), f"Profile output file {profile_path} is missing."

    with open(profile_path, 'r') as f:
        content = f.read()

    # Check for typical /usr/bin/time -v output markers
    assert "Maximum resident set size" in content, "profile.txt does not contain 'Maximum resident set size', indicating /usr/bin/time -v was not used correctly."
    assert "User time" in content, "profile.txt does not contain 'User time', indicating /usr/bin/time -v was not used correctly."