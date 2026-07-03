# test_final_state.py
import os

def test_regression_info_correct():
    user_file = "/home/user/regression_info.txt"
    expected_file = "/tmp/expected_solution.txt"

    assert os.path.isfile(user_file), f"File {user_file} does not exist. Did you create it?"
    assert os.path.isfile(expected_file), f"Expected solution file {expected_file} is missing from the system."

    with open(user_file, "r") as f:
        user_lines = [line.strip() for line in f if line.strip()]

    with open(expected_file, "r") as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    assert len(user_lines) == 2, f"Expected exactly 2 non-empty lines in {user_file}, found {len(user_lines)}."

    user_dict = {}
    for line in user_lines:
        assert "=" in line, f"Line '{line}' is not in the format KEY=VALUE."
        k, v = line.split("=", 1)
        user_dict[k.strip()] = v.strip()

    expected_dict = {}
    for line in expected_lines:
        if "=" in line:
            k, v = line.split("=", 1)
            expected_dict[k.strip()] = v.strip()

    assert "COMMIT" in user_dict, "COMMIT key missing in regression_info.txt."
    assert "TOKEN" in user_dict, "TOKEN key missing in regression_info.txt."

    assert user_dict["COMMIT"] == expected_dict["COMMIT"], f"Incorrect COMMIT hash. Expected {expected_dict['COMMIT']}, got {user_dict['COMMIT']}."
    assert user_dict["TOKEN"] == expected_dict["TOKEN"], f"Incorrect TOKEN. Expected {expected_dict['TOKEN']}, got {user_dict['TOKEN']}."