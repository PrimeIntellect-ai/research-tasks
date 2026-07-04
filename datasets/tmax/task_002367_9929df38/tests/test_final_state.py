# test_final_state.py

import os
import stat

def test_extractor_source_exists():
    src_path = "/home/user/extractor.c"
    assert os.path.isfile(src_path), f"C source file {src_path} is missing."

def test_extractor_executable_exists():
    exe_path = "/home/user/extractor"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {exe_path} is not executable."

def test_recovered_timeline():
    out_path = "/home/user/recovered_timeline.csv"
    assert os.path.isfile(out_path), f"Output file {out_path} is missing."

    expected_lines = [
        "1600000000,10,50",
        "1600000025,15,100",
        "1600000050,12,20",
        "1600000100,10,10"
    ]

    with open(out_path, "r") as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {out_path} do not match the expected timeline.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )