# test_final_state.py
import os

def test_spectrum_csv_exists_and_correct():
    csv_path = "/home/user/spectrum.csv"
    assert os.path.isfile(csv_path), f"{csv_path} does not exist. Did you run the simulation and write the output?"

    expected_lines = [
        "400,0",
        "405,0",
        "410,2",
        "415,6",
        "420,11",
        "425,18",
        "430,49",
        "435,76",
        "440,110",
        "445,190",
        "450,292",
        "455,420",
        "460,656",
        "465,952",
        "470,1282",
        "475,1551",
        "480,1832",
        "485,2148",
        "490,2308",
        "495,2446",
        "500,2400",
        "505,2410",
        "510,2112",
        "515,1838",
        "520,1523",
        "525,1166",
        "530,942",
        "535,699",
        "540,432",
        "545,296",
        "550,192",
        "555,108",
        "560,70",
        "565,39",
        "570,16",
        "575,7",
        "580,2",
        "585,0",
        "590,0",
        "595,1"
    ]

    with open(csv_path, "r") as f:
        # Read lines, strip whitespace, and ignore empty lines at the end
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 40, f"Expected exactly 40 lines in {csv_path}, found {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i + 1} mismatch: expected '{expected}', got '{actual}'"