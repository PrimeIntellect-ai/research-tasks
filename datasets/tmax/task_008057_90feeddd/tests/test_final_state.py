# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_extracted_flag():
    flag_path = "/home/user/extracted_flag.txt"
    assert os.path.isfile(flag_path), f"{flag_path} does not exist."
    with open(flag_path, "r") as f:
        content = f.read().strip()
    assert content == "FLAG{F0r3ns1cs_M4st3r_X0R}", "The extracted flag is incorrect."

def test_test_runner_script():
    script_path = "/home/user/test_runner.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"test_runner.sh failed with return code {result.returncode}."

def test_executable_exists():
    exe_path = "/home/user/forensics_tool/carver"
    assert os.path.isfile(exe_path), "The 'carver' executable was not built."
    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{exe_path} is not executable."

def test_makefile_fixed():
    makefile_path = "/home/user/forensics_tool/Makefile"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "decoder.o" in content, "Makefile does not reference decoder.o."

    # Check if carver target links decoder.o
    lines = content.splitlines()
    carver_target_found = False
    for i, line in enumerate(lines):
        if line.startswith("carver:"):
            assert "decoder.o" in line, "Makefile 'carver' target does not depend on decoder.o."
            assert "decoder.o" in lines[i+1], "Makefile 'carver' target does not link decoder.o."
            carver_target_found = True
            break
    assert carver_target_found, "Makefile does not contain a 'carver' target."

def test_decoder_h_fixed():
    decoder_h_path = "/home/user/forensics_tool/decoder.h"
    with open(decoder_h_path, "r") as f:
        content = f.read()
    assert "__attribute__((packed))" in content.replace(" ", "").replace("\t", "").replace("\n", ""), "decoder.h struct EvidenceHeader is missing __attribute__((packed))."

def test_decoder_c_fixed():
    decoder_c_path = "/home/user/forensics_tool/decoder.c"
    with open(decoder_c_path, "r") as f:
        content = f.read()

    # Check for off-by-one fix
    assert "i <= len" not in content, "decoder.c still contains the off-by-one bug (i <= len)."
    assert "i < len" in content, "decoder.c does not contain the fixed loop boundary (i < len)."

    # Check for convergence fix
    assert "left = mid;" not in content, "decoder.c still contains the convergence bug (left = mid;)."
    assert "right = mid;" not in content, "decoder.c still contains the convergence bug (right = mid;)."
    assert "left = mid + 1" in content or "left=mid+1" in content.replace(" ", ""), "decoder.c does not properly increment left in binary search."
    assert "right = mid - 1" in content or "right=mid-1" in content.replace(" ", ""), "decoder.c does not properly decrement right in binary search."

def test_carver_output():
    exe_path = "/home/user/forensics_tool/carver"
    evidence_path = "/home/user/data/evidence.bin"
    result = subprocess.run([exe_path, evidence_path], capture_output=True, text=True)
    assert result.returncode == 0, "carver executable failed to run."
    assert "FLAG{F0r3ns1cs_M4st3r_X0R}" in result.stdout, "carver output did not contain the correct decoded flag."