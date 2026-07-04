# test_final_state.py
import os

def test_extractor_cpp_exists():
    assert os.path.isfile("/home/user/extractor.cpp"), "The C++ source file /home/user/extractor.cpp is missing."

def test_extractor_executable_exists():
    assert os.path.isfile("/home/user/extractor"), "The compiled executable /home/user/extractor is missing."
    assert os.access("/home/user/extractor", os.X_OK), "The file /home/user/extractor is not executable."

def test_curation_report_exists_and_correct():
    report_path = "/home/user/curation_report.txt"
    assert os.path.isfile(report_path), f"The report file {report_path} is missing."

    expected_lines = [
        "/home/user/artifacts/alpha.bin - 0102030405060708090A",
        "/home/user/artifacts/beta.bin - INVALID",
        "/home/user/artifacts/epsilon.bin - INVALID",
        "/home/user/artifacts/zeta.bin - DEADBEEFCAFEBABE"
    ]

    with open(report_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in the report, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual.strip()}'"