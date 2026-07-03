# test_final_state.py
import os
import sys
import importlib.util

def test_generate_fixture_script_exists():
    script_path = "/home/user/generate_fixture.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

def test_test_fixture_file_exists():
    fixture_path = "/home/user/test_fixture.py"
    assert os.path.isfile(fixture_path), f"Expected output file {fixture_path} does not exist."

def test_test_fixture_content():
    fixture_path = "/home/user/test_fixture.py"
    assert os.path.isfile(fixture_path), "Fixture file missing."

    # Dynamically import the generated fixture file
    spec = importlib.util.spec_from_file_location("test_fixture", fixture_path)
    test_fixture = importlib.util.module_from_spec(spec)
    sys.modules["test_fixture"] = test_fixture
    try:
        spec.loader.exec_module(test_fixture)
    except Exception as e:
        assert False, f"Failed to import {fixture_path}: {e}"

    assert hasattr(test_fixture, "valid_targets"), "The function 'valid_targets' is missing from test_fixture.py"

    # Check if it has the pytest.fixture decorator (checking if pytest is imported is a good proxy, 
    # but we can just call the function to check its logic)
    try:
        targets = test_fixture.valid_targets()
    except Exception as e:
        assert False, f"Calling valid_targets() raised an exception: {e}"

    expected_targets = ["Phone_C", "Phone_D"]
    assert targets == expected_targets, f"Expected valid_targets() to return {expected_targets}, but got {targets}"