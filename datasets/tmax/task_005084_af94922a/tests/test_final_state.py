# test_final_state.py
import os
import csv

def test_valid_primers_tm_output():
    output_file = "/home/user/valid_primers_tm.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output CSV is empty."
    header = rows[0]
    assert header == ["primer_id", "Tm"], f"Header is incorrect. Expected ['primer_id', 'Tm'], got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 2, f"Expected exactly 2 data rows for valid unique primers, got {len(data_rows)}."

    # Check sorting
    primer_ids = [row[0] for row in data_rows]
    assert primer_ids == ["P1", "P4"], f"Expected primer_ids to be ['P1', 'P4'] (sorted alphabetically), got {primer_ids}."

    # Check Tm values and rounding
    try:
        p1_tm = float(data_rows[0][1])
        p4_tm = float(data_rows[1][1])
    except ValueError:
        assert False, "Tm values in the CSV must be numeric."

    assert abs(p1_tm - 65.20) <= 0.05, f"P1 Tm value {p1_tm} is outside the acceptable range (65.20 +/- 0.05)."
    assert abs(p4_tm - 68.45) <= 0.05, f"P4 Tm value {p4_tm} is outside the acceptable range (68.45 +/- 0.05)."

    # Verify exact 2 decimal places string format
    p1_str = data_rows[0][1].strip()
    p4_str = data_rows[1][1].strip()

    assert '.' in p1_str and len(p1_str.split('.')[1]) == 2, f"P1 Tm '{p1_str}' is not rounded to exactly 2 decimal places."
    assert '.' in p4_str and len(p4_str.split('.')[1]) == 2, f"P4 Tm '{p4_str}' is not rounded to exactly 2 decimal places."