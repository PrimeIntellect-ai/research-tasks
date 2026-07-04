# test_final_state.py

import os
import sys
import sqlite3
import json

def test_app_logic_fixed():
    app_path = '/home/user/app.py'
    assert os.path.exists(app_path), "app.py is missing"

    # Dynamically import app.py to test the modified function
    sys.path.insert(0, '/home/user')
    try:
        import app
    except Exception as e:
        assert False, f"Failed to import app.py: {e}"

    assert hasattr(app, 'validate_user_data'), "validate_user_data function is missing from app.py"

    # Test valid data
    try:
        result = app.validate_user_data('{"status": "active", "points": 150}')
        assert result is True, "validate_user_data should return True for valid data"
    except Exception as e:
        assert False, f"validate_user_data raised an exception for valid data: {e}"

    # Test invalid data (negative points)
    try:
        app.validate_user_data('{"status": "active", "points": -50}')
        assert False, "validate_user_data did not raise ValueError for negative points"
    except ValueError:
        pass # Expected behavior
    except Exception as e:
        assert False, f"validate_user_data raised unexpected exception for negative points: {type(e).__name__}"

def test_regression_test_file():
    test_file = '/home/user/test_regression.py'
    assert os.path.exists(test_file), "Regression test file missing"

    with open(test_file, 'r') as f:
        content = f.read()

    # Retrieve the expected metadata string from the database
    db_path = "/home/user/users.db"
    assert os.path.exists(db_path), "Database file missing"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT metadata FROM users WHERE id=9942;")
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "User ID 9942 is missing from the database"
    metadata_str = row[0]

    # Check if the test file uses the exact metadata string (ignoring whitespace differences)
    assert metadata_str.replace(" ", "") in content.replace(" ", ""), "test_regression.py does not use the extracted metadata string"
    assert "ValueError" in content, "test_regression.py does not assert ValueError"
    assert "unittest" in content, "test_regression.py does not use the unittest framework"
    assert "TestUserValidation" in content, "test_regression.py is missing the TestUserValidation class"
    assert "test_negative_points_raises_error" in content, "test_regression.py is missing the test_negative_points_raises_error method"

def test_test_result_log():
    log_file = '/home/user/test_result.log'
    assert os.path.exists(log_file), "Test result log missing"

    with open(log_file, 'r') as f:
        content = f.read()

    assert "OK" in content, "Regression test log does not indicate success ('OK' not found)"
    assert "FAILED" not in content, "Regression test log indicates failure ('FAILED' found)"
    assert "Ran 1 test" in content or "Ran" in content, "Regression test log does not appear to be valid unittest output"