# test_final_state.py

import os
import pytest

def test_predictions_csv_correct():
    path = "/home/user/predictions.csv"
    assert os.path.isfile(path), f"File {path} is missing. Did you compile and run the fixed C++ code?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = """id,prediction
101,7.6
102,2.3
103,17.1
104,0.1"""

    assert content == expected, f"Content of {path} is incorrect.\nExpected:\n{expected}\n\nActual:\n{content}"