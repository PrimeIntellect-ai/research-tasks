# test_final_state.py
import os

def test_final_state():
    output_csv_path = "/home/user/output.csv"
    assert os.path.isfile(output_csv_path), f"Expected output file {output_csv_path} does not exist."

    with open(output_csv_path, "r") as f:
        content = f.read().strip()

    expected_content = """ts,reading,is_anomaly
10,205.0,0
20,230.0,0
30,255.0,0
40,400.0,1
50,410.0,0"""

    assert content == expected_content, (
        f"Content of {output_csv_path} does not match expected.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Actual:\n{content}"
    )