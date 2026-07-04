# test_final_state.py

import os
import filecmp

def test_final_chain_exists():
    path = "/home/user/final_chain.csv"
    assert os.path.isfile(path), f"Expected file {path} does not exist. Did you copy your chain.csv to final_chain.csv?"

def test_final_chain_matches_reference():
    final_chain = "/home/user/final_chain.csv"
    reference_chain = "/home/user/reference_chain.csv"

    assert os.path.isfile(final_chain), "final_chain.csv is missing."
    assert os.path.isfile(reference_chain), "reference_chain.csv is missing."

    with open(final_chain, 'r') as f1, open(reference_chain, 'r') as f2:
        final_lines = f1.readlines()
        ref_lines = f2.readlines()

    assert len(final_lines) == len(ref_lines), "final_chain.csv does not have the same number of lines as reference_chain.csv."

    for i, (l1, l2) in enumerate(zip(final_lines, ref_lines)):
        assert l1.strip() == l2.strip(), f"Mismatch at line {i+1}:\nExpected: {l2.strip()}\nGot: {l1.strip()}"

def test_sampler_cpp_modified():
    sampler_path = "/home/user/sampler.cpp"
    assert os.path.isfile(sampler_path), "sampler.cpp is missing."
    with open(sampler_path, 'r') as f:
        content = f.read()

    # Check if kahan summation logic might be present (e.g., a variable for the compensation 'c' or 'y')
    # Since variable names can vary, just check if the file was modified from the naive version.
    naive_snippet = "sum += -0.5 * (x - mu) * (x - mu);"
    assert naive_snippet not in content or "c =" in content or "y =" in content, "sampler.cpp still appears to use naive summation."