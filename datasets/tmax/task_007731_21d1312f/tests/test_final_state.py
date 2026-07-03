# test_final_state.py

import os
import stat

def test_summary_txt():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Apollo_Lunar: 1\nArtemis_Base: 1\nGemini: 2"

    # Compare lines ignoring trailing whitespace or empty lines
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Summary file content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_symlinks():
    expected_symlinks = {
        "/home/user/organized/json/Apollo_Lunar_meta1.json": "/home/user/raw_data/dir1/meta1.json",
        "/home/user/organized/json/Gemini_meta3.json": "/home/user/raw_data/dir3/meta3.json",
        "/home/user/organized/xml/Gemini_meta2.xml": "/home/user/raw_data/dir1/dir2/meta2.xml",
        "/home/user/organized/csv/Artemis_Base_data.csv": "/home/user/raw_data/dir3/data.csv"
    }

    for symlink_path, target_path in expected_symlinks.items():
        assert os.path.islink(symlink_path), f"Expected symlink at {symlink_path} does not exist or is not a symlink."
        actual_target = os.readlink(symlink_path)
        assert actual_target == target_path, f"Symlink {symlink_path} points to {actual_target}, expected {target_path}."

def test_script_exists_and_executable():
    script_path = "/home/user/organize.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."