# test_final_state.py
import os
import sys
import json
import pytest
import importlib.util

WORKSPACE_DIR = "/home/user/workspace"

def test_c_library_built():
    so_path = os.path.join(WORKSPACE_DIR, "c_src", "libhtmlparser.so")
    assert os.path.isfile(so_path), f"C library was not built at {so_path}"

def test_python_package_installed():
    try:
        import fast_sanitizer
    except ImportError:
        pytest.fail("fast_sanitizer package is not installed or importable.")

    # Test if it actually works and uses the patched C library
    try:
        res = fast_sanitizer.sanitize("eval(1)")
        assert "SAFE_" in res, "The C library does not seem to be patched correctly."
    except Exception as e:
        pytest.fail(f"fast_sanitizer.sanitize failed: {e}")

def test_payloads_py_exists_and_correct():
    payloads_path = os.path.join(WORKSPACE_DIR, "tests", "payloads.py")
    assert os.path.isfile(payloads_path), f"File {payloads_path} is missing."

    spec = importlib.util.spec_from_file_location("payloads", payloads_path)
    payloads = importlib.util.module_from_spec(spec)
    sys.modules["payloads"] = payloads
    try:
        spec.loader.exec_module(payloads)
    except Exception as e:
        pytest.fail(f"Failed to execute payloads.py: {e}")

    assert hasattr(payloads, "get_payloads"), "get_payloads function missing in payloads.py"
    data = payloads.get_payloads()
    assert isinstance(data, list), "get_payloads should return a list"
    assert len(data) == 3, "get_payloads should return exactly 3 items"
    assert data[0].get("id") == 1, "First payload ID should be 1"
    assert data[0].get("payload") == "<script>alert(1)</script>", "First payload string mismatch"

def test_results_xml_exists():
    xml_path = os.path.join(WORKSPACE_DIR, "tests", "results.xml")
    assert os.path.isfile(xml_path), f"XML results file {xml_path} is missing."

def test_summary_json_correct():
    json_path = os.path.join(WORKSPACE_DIR, "summary.json")
    assert os.path.isfile(json_path), f"JSON summary file {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not valid JSON.")

    assert isinstance(data, list), "summary.json should contain a JSON array."
    assert len(data) == 3, "summary.json should have exactly 3 entries."

    expected_data = [
        {
            "id": 1,
            "original": "<script>alert(1)</script>",
            "sanitized": "<script>alert(1)</script>",
            "is_safe": False
        },
        {
            "id": 2,
            "original": "<img src=x onerror=alert(1)>",
            "sanitized": "<img src=x onsafe =alert(1)>",
            "is_safe": True
        },
        {
            "id": 3,
            "original": "javascript:eval('alert(1)')",
            "sanitized": "javascript:SAFE_('alert(1)')",
            "is_safe": True
        }
    ]

    for i, expected in enumerate(expected_data):
        assert data[i].get("id") == expected["id"], f"Item {i} 'id' mismatch. Expected {expected['id']}, got {data[i].get('id')}."
        assert data[i].get("original") == expected["original"], f"Item {i} 'original' mismatch."
        assert data[i].get("sanitized") == expected["sanitized"], f"Item {i} 'sanitized' mismatch."
        assert data[i].get("is_safe") is expected["is_safe"], f"Item {i} 'is_safe' mismatch. Expected {expected['is_safe']}, got {data[i].get('is_safe')}."