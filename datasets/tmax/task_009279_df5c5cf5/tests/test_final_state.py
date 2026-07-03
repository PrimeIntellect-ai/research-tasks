# test_final_state.py
import os
import sys
import pytest

def test_extracted_payload():
    path = "/home/user/ticket_4092/extracted_payload.txt"
    assert os.path.exists(path), "extracted_payload.txt is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    expected = "435553547c313530303023696e76616c69645f757466385fff"
    assert content.lower() == expected, f"extracted_payload.txt content is incorrect. Expected {expected}, got {content}"

def test_processor_fixes():
    sys.path.insert(0, "/home/user/ticket_4092")
    try:
        import processor
    except ImportError:
        pytest.fail("Could not import processor.py")

    # Test memory exhaustion fix (length > 1000)
    with pytest.raises(ValueError, match="Payload too large"):
        processor.deserialize(b"CUST|1001#abc")

    # Test encoding crash fix (invalid utf-8)
    try:
        res = processor.deserialize(b"CUST|4#\xff\xff\xff\xff")
    except UnicodeDecodeError:
        pytest.fail("UnicodeDecodeError was raised. The decoding step does not gracefully handle invalid bytes.")

    assert isinstance(res, str), "deserialize should still return a string when processing invalid utf-8 bytes."

def test_regression_test_file():
    path = "/home/user/ticket_4092/test_processor.py"
    assert os.path.exists(path), "test_processor.py is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "def test_regression_cve_2023_memory" in content, "test_regression_cve_2023_memory() function is missing in test_processor.py."
    assert "ValueError" in content, "The test does not seem to check for ValueError."
    assert "Payload too large" in content, "The test does not seem to check for the 'Payload too large' message."