# test_final_state.py

import os

PIPELINE_DIR = "/home/user/pipeline"

def test_final_score_correct():
    final_score_path = os.path.join(PIPELINE_DIR, "final_score.txt")
    assert os.path.isfile(final_score_path), f"File {final_score_path} does not exist. Did the pipeline finish?"

    with open(final_score_path, "r") as f:
        content = f.read().strip()

    assert content == "105.2432", f"Expected final_score.txt to contain '105.2432', but got '{content}'."

def test_output_csv_matches_expected():
    output_csv = os.path.join(PIPELINE_DIR, "output.csv")
    expected_csv = os.path.join(PIPELINE_DIR, "expected.csv")

    assert os.path.isfile(output_csv), f"File {output_csv} does not exist. Did transform.py run successfully?"
    assert os.path.isfile(expected_csv), f"File {expected_csv} is missing. Do not delete the truth data."

    with open(output_csv, "r") as f:
        output_content = f.read().strip()

    with open(expected_csv, "r") as f:
        expected_content = f.read().strip()

    assert output_content == expected_content, "The content of output.csv does not exactly match expected.csv."