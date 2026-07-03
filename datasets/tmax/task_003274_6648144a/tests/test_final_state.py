# test_final_state.py
import os
import pytest

BASE_DIR = "/home/user/build_system"

def test_make_sh_exists_and_executable():
    make_sh = os.path.join(BASE_DIR, "make.sh")
    assert os.path.isfile(make_sh), f"{make_sh} does not exist."
    assert os.access(make_sh, os.X_OK), f"{make_sh} is not executable."

def test_final_output_log():
    log_path = os.path.join(BASE_DIR, "final_output.log")
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "Source D Patched\nSource B Patched\nSource D Patched\nSource C\nSource A"
    assert content == expected, f"final_output.log content is incorrect.\nGot:\n{content}\nExpected:\n{expected}"

def test_out_a_matches_log():
    out_a = os.path.join(BASE_DIR, "out", "A.out")
    log_path = os.path.join(BASE_DIR, "final_output.log")

    assert os.path.isfile(out_a), f"{out_a} does not exist."
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(out_a, "r") as f1, open(log_path, "r") as f2:
        assert f1.read().strip() == f2.read().strip(), "out/A.out content does not match final_output.log"

def test_patched_sources():
    b_txt = os.path.join(BASE_DIR, "src", "B.txt")
    d_txt = os.path.join(BASE_DIR, "src", "D.txt")

    with open(b_txt, "r") as f:
        assert f.read().strip() == "Source B Patched", "src/B.txt was not correctly patched."

    with open(d_txt, "r") as f:
        assert f.read().strip() == "Source D Patched", "src/D.txt was not correctly patched."

def test_unpatched_sources_unchanged():
    a_txt = os.path.join(BASE_DIR, "src", "A.txt")
    c_txt = os.path.join(BASE_DIR, "src", "C.txt")

    with open(a_txt, "r") as f:
        assert f.read().strip() == "Source A", "src/A.txt should not have been modified."

    with open(c_txt, "r") as f:
        assert f.read().strip() == "Source C", "src/C.txt should not have been modified."