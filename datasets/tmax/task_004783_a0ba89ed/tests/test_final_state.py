# test_final_state.py
import os

def test_correct_sum_file():
    sum_file = '/home/user/correct_sum.txt'
    assert os.path.exists(sum_file), f"File {sum_file} does not exist. Did you save the result?"
    assert os.path.isfile(sum_file), f"{sum_file} is not a file."

    with open(sum_file, 'r') as f:
        content = f.read().strip()

    assert content == "14000000000", f"Expected sum '14000000000', but got '{content}' in {sum_file}."

def test_calculate_sum_script_fixed():
    script_file = '/home/user/calculate_sum.py'
    assert os.path.exists(script_file), f"File {script_file} does not exist."

    with open(script_file, 'r') as f:
        content = f.read()

    assert "struct.unpack('<i'" not in content and 'struct.unpack("<i"' not in content, \
        "The script still contains the buggy '<i' format specifier for signed integers."
    assert "struct.unpack('<I'" in content or 'struct.unpack("<I"' in content, \
        "The script does not contain the fixed '<I' format specifier for unsigned integers."