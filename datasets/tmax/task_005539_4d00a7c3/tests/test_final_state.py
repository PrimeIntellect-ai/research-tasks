# test_final_state.py
import os
import subprocess
import xml.etree.ElementTree as ET
import pytest

BASE_DIR = "/home/user/ws_calc"

def test_shared_library_exists():
    """Verify that the shared library was built and exists at the expected path."""
    lib_path = os.path.join(BASE_DIR, "build", "libcalc.so")
    assert os.path.isfile(lib_path), f"Shared library not found at {lib_path}. Did you build it?"

def test_process_data_exported_c_linkage():
    """Verify that process_data is exported with C linkage (unmangled)."""
    lib_path = os.path.join(BASE_DIR, "build", "libcalc.so")
    assert os.path.isfile(lib_path), "Shared library is missing."

    try:
        output = subprocess.check_output(["nm", "-D", lib_path], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run nm on {lib_path}: {e}")
    except FileNotFoundError:
        pytest.fail("The 'nm' command is not available.")

    lines = output.splitlines()
    found = False
    for line in lines:
        parts = line.split()
        if len(parts) >= 3 and parts[1] == "T" and parts[2] == "process_data":
            found = True
            break

    assert found, "Function 'process_data' is not exported with C linkage (unmangled). Did you forget 'extern \"C\"'?"

def test_test_results_xml_exists():
    """Verify that the pytest JUnit XML report was generated."""
    xml_path = os.path.join(BASE_DIR, "test_results.xml")
    assert os.path.isfile(xml_path), f"Test results XML not found at {xml_path}. Did you run pytest with --junitxml?"

def test_test_results_xml_passed():
    """Verify that the test suite ran and passed according to the XML report."""
    xml_path = os.path.join(BASE_DIR, "test_results.xml")
    assert os.path.isfile(xml_path), "Test results XML is missing."

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        pytest.fail(f"Failed to parse {xml_path} as XML: {e}")

    # JUnit XML root is usually <testsuites> or <testsuite>
    if root.tag == "testsuites":
        testsuites = root.findall("testsuite")
    elif root.tag == "testsuite":
        testsuites = [root]
    else:
        pytest.fail(f"Unexpected root tag '{root.tag}' in {xml_path}")

    total_tests = 0
    total_failures = 0
    total_errors = 0

    for ts in testsuites:
        total_tests += int(ts.attrib.get("tests", 0))
        total_failures += int(ts.attrib.get("failures", 0))
        total_errors += int(ts.attrib.get("errors", 0))

    assert total_tests > 0, "No tests were reported as run in the XML results."
    assert total_failures == 0, f"Expected 0 test failures, but found {total_failures}."
    assert total_errors == 0, f"Expected 0 test errors, but found {total_errors}."

def test_test_ws_py_exists():
    """Verify that the test integration file was created."""
    test_file_path = os.path.join(BASE_DIR, "tests", "test_ws.py")
    assert os.path.isfile(test_file_path), f"Integration test file not found at {test_file_path}."