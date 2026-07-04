# test_final_state.py

import os
import tarfile
import pytest

def test_executable_exists():
    executable_path = "/home/user/src/analyze"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist. Did you compile the C program?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_results_csv_exists_and_correct():
    results_path = "/home/user/artifacts/results.csv"
    assert os.path.isfile(results_path), f"File {results_path} does not exist. Did you run the C program?"

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "EXP_101,0.7000",
        "EXP_102,0.2857",
        "EXP_103,0.9167",
        "EXP_104,0.5000"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.csv, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in results.csv is incorrect. Expected '{expected}', got '{actual}'."

def test_tarball_exists_and_contains_artifacts():
    tarball_path = "/home/user/artifacts.tar.gz"
    assert os.path.isfile(tarball_path), f"Tarball {tarball_path} does not exist."
    assert tarfile.is_tarfile(tarball_path), f"File {tarball_path} is not a valid tar archive."

    with tarfile.open(tarball_path, "r:gz") as tar:
        members = tar.getnames()

        # Check that artifacts directory is at the root of the tarball
        # It should contain something like 'artifacts/results.csv'
        has_results_csv = any(m.endswith("artifacts/results.csv") for m in members)
        assert has_results_csv, "Tarball does not contain 'artifacts/results.csv'. Make sure the 'artifacts' directory is at the root of the tarball."

        # Verify the contents of the results.csv inside the tarball
        for member in tar.getmembers():
            if member.name.endswith("artifacts/results.csv"):
                f = tar.extractfile(member)
                assert f is not None, "Could not extract results.csv from tarball."
                content = f.read().decode('utf-8').splitlines()
                lines = [line.strip() for line in content if line.strip()]

                expected_lines = [
                    "EXP_101,0.7000",
                    "EXP_102,0.2857",
                    "EXP_103,0.9167",
                    "EXP_104,0.5000"
                ]
                assert lines == expected_lines, "The results.csv inside the tarball does not match the expected output."
                break