# test_final_state.py

import os

def test_jq_installed():
    jq_bin = "/home/user/bin/jq"
    assert os.path.exists(jq_bin), f"{jq_bin} does not exist."
    assert os.path.isfile(jq_bin), f"{jq_bin} is not a file."
    assert os.access(jq_bin, os.X_OK), f"{jq_bin} is not executable."

def test_processed_events_csv():
    output_file = "/home/user/processed_events.csv"
    assert os.path.exists(output_file), f"Output file {output_file} is missing."
    assert os.path.isfile(output_file), f"{output_file} is not a file."

    expected_csv = (
        "userId,action\n"
        "101,login\n"
        "204,purchase\n"
        "99,logout"
    )

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == expected_csv, (
        f"Content of {output_file} is incorrect.\n"
        f"Expected:\n{expected_csv}\n"
        f"Got:\n{content}"
    )