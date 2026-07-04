# test_final_state.py
import os

def test_overhang_extracted():
    overhang_file = "/home/user/overhang.txt"
    seq_file = "/home/user/sequence.txt"

    assert os.path.exists(overhang_file), f"File {overhang_file} does not exist."
    assert os.path.exists(seq_file), f"File {seq_file} does not exist."

    with open(seq_file, "r") as f:
        seq = f.read().strip()

    idx = seq.find("GGTCTC")
    assert idx != -1, "BsaI site not found in sequence.txt."

    next_4 = seq[idx+6:idx+10]
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    expected_overhang = "".join(complement.get(base, base) for base in reversed(next_4))

    with open(overhang_file, "r") as f:
        actual_overhang = f.read().strip()

    assert actual_overhang == expected_overhang, f"Expected overhang '{expected_overhang}', but got '{actual_overhang}'."

def test_qpcr_col_max_r():
    result_file = "/home/user/col_max_r.txt"
    truth_file = "/home/user/.truth_col_max_r"

    assert os.path.exists(result_file), f"File {result_file} does not exist."
    assert os.path.exists(truth_file), f"Truth file {truth_file} does not exist. Cannot verify."

    with open(truth_file, "r") as f:
        expected_content = f.read().strip()

    with open(result_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Expected col_max_r content '{expected_content}', but got '{actual_content}'."