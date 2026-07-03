# test_final_state.py

import os
import re

def test_mcmc_c_exists():
    assert os.path.isfile("/home/user/mcmc_Z.c"), "The file /home/user/mcmc_Z.c does not exist."

def test_build_script_exists_and_executable():
    script_path = "/home/user/build_and_run.sh"
    assert os.path.isfile(script_path), f"The file {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The file {script_path} is not executable."

def test_result_file_exists():
    assert os.path.isfile("/home/user/result.txt"), "The file /home/user/result.txt does not exist."

def test_result_content():
    with open("/home/user/result.txt", "r") as f:
        content = f.read().strip()

    expected = "Z_val: 0.501253"
    assert expected in content, f"Expected '{expected}' in /home/user/result.txt, but got: {content}"

def test_kahan_summation_implemented():
    with open("/home/user/mcmc_Z.c", "r") as f:
        content = f.read()

    # Heuristic check for Kahan summation logic (e.g., tracking a correction term)
    # Looking for signs of compensation calculation: c =, err =, comp =, or y =, t =
    pattern = re.compile(r'\b(c|err|comp|y|t)\s*[-+*\/]?=', re.IGNORECASE)

    # Also look for a loop doing the summation
    has_compensation = pattern.search(content) is not None

    assert has_compensation, "Could not find evidence of Kahan summation (e.g. compensation variable updates) in /home/user/mcmc_Z.c."