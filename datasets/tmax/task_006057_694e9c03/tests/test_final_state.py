# test_final_state.py

import os
import struct
import xml.etree.ElementTree as ET
import pytest

def get_expected_violations():
    quotas_path = '/home/user/quotas.csv'
    wal_path = '/home/user/allocations.wal'

    # Read quotas
    quotas = {}
    if os.path.exists(quotas_path):
        with open(quotas_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        try:
                            uid = int(parts[0])
                            quota = int(parts[1])
                            quotas[uid] = quota
                        except ValueError:
                            pass

    # Read WAL and calculate usage
    usage = {}
    if os.path.exists(wal_path):
        with open(wal_path, 'rb') as f:
            while True:
                record = f.read(16)
                if not record or len(record) < 16:
                    break
                ts, uid, delta = struct.unpack('<QIi', record)
                usage[uid] = usage.get(uid, 0) + delta

    # Determine violations
    violations = []
    for uid, used in usage.items():
        if uid in quotas and used > quotas[uid]:
            violations.append((uid, used, quotas[uid]))

    # Sort by user_id ascending
    violations.sort(key=lambda x: x[0])
    return violations

def test_violations_xml_exists():
    xml_path = '/home/user/violations.xml'
    assert os.path.isfile(xml_path), f"Expected output file {xml_path} does not exist."

def test_violations_xml_content():
    xml_path = '/home/user/violations.xml'
    assert os.path.isfile(xml_path), f"Cannot test content, {xml_path} is missing."

    expected_violations = get_expected_violations()

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        pytest.fail(f"Failed to parse {xml_path} as XML: {e}")

    assert root.tag == "violations", f"Root element should be <violations>, got <{root.tag}>"

    actual_violations = []
    for child in root:
        assert child.tag == "violation", f"Expected <violation> tag, got <{child.tag}>"
        try:
            uid = int(child.attrib.get("user_id", -1))
            used = int(child.attrib.get("used", -1))
            quota = int(child.attrib.get("quota", -1))
            actual_violations.append((uid, used, quota))
        except ValueError:
            pytest.fail(f"Invalid attribute values in violation tag: {child.attrib}")

    assert len(actual_violations) == len(expected_violations), \
        f"Expected {len(expected_violations)} violations, found {len(actual_violations)}."

    for i, (expected, actual) in enumerate(zip(expected_violations, actual_violations)):
        assert expected == actual, \
            f"Violation mismatch at index {i}. Expected (user_id={expected[0]}, used={expected[1]}, quota={expected[2]}), " \
            f"got (user_id={actual[0]}, used={actual[1]}, quota={actual[2]})."

def test_c_source_and_executable_exist():
    c_source = '/home/user/check_quotas.c'
    executable = '/home/user/check_quotas'

    assert os.path.isfile(c_source), f"C source file {c_source} is missing."
    assert os.path.isfile(executable), f"Compiled executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."