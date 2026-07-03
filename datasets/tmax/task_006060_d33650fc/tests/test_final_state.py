# test_final_state.py
import os
import re

def test_projected_nt_exists():
    path = "/home/user/projected.nt"
    assert os.path.isfile(path), f"File {path} does not exist. The script did not generate the output file."

def test_projected_nt_contents():
    path = "/home/user/projected.nt"
    with open(path, "r") as f:
        lines = f.readlines()

    actual_subjects = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match N-Triples format: <subject> <predicate> <object> .
        match = re.match(r'^(<[^>]+>)\s+(<[^>]+>)\s+(<[^>]+>)\s*\.$', line)
        assert match, f"Line does not match N-Triples format: '{line}'"

        subj, pred, obj = match.groups()

        expected_pred = "<http://example.org/org#deepReportsTo>"
        expected_obj = "<http://example.org/CEO>"

        assert pred == expected_pred, f"Unexpected predicate '{pred}' found. Expected '{expected_pred}'."
        assert obj == expected_obj, f"Unexpected object '{obj}' found. Expected '{expected_obj}'."

        actual_subjects.add(subj)

    expected_subjects = {
        "<http://example.org/Bob>",
        "<http://example.org/Charlie>",
        "<http://example.org/Dave>",
        "<http://example.org/Frank>",
        "<http://example.org/Grace>"
    }

    missing = expected_subjects - actual_subjects
    extra = actual_subjects - expected_subjects

    assert not missing, f"Missing deep reports in output: {missing}"
    assert not extra, f"Extra incorrect reports found in output: {extra}"
    assert actual_subjects == expected_subjects