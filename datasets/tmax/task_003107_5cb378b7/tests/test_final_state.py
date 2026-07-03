# test_final_state.py
import os
import xml.etree.ElementTree as ET
import pytest

XML_PATH = '/home/user/updated_translations.xml'

def test_xml_file_exists():
    assert os.path.isfile(XML_PATH), f"File {XML_PATH} does not exist."

def test_xml_structure_and_counts():
    try:
        tree = ET.parse(XML_PATH)
    except ET.ParseError as e:
        pytest.fail(f"Failed to parse XML: {e}")

    root = tree.getroot()
    assert root.tag == "translations", "Root element must be <translations>"

    translations = root.findall('translation')
    assert len(translations) == 4, f"Expected exactly 4 <translation> elements, found {len(translations)}"

    ids = [int(t.get('id')) for t in translations]
    assert ids == [1, 2, 3, 4], f"Translations must be sorted by id as integers. Got ids: {ids}"

def test_xml_content_and_computations():
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    expected_confidences = {
        "1": 0.995,
        "2": 0.857,
        "3": 1.000,
        "4": 0.850
    }

    for t in root.findall('translation'):
        t_id = t.get('id')
        conf_str = t.get('confidence')

        assert conf_str is not None, f"Missing 'confidence' attribute for id {t_id}"

        try:
            conf = float(conf_str)
        except ValueError:
            pytest.fail(f"Confidence for id {t_id} is not a valid float: {conf_str}")

        source_elem = t.find('source')
        assert source_elem is not None, f"Missing <source> for id {t_id}"
        source = source_elem.text or ""

        if t_id == "2":
            assert "é" in source, f"Unicode decoding failed for ID 2. Expected 'é' in source, got: {source}"
        if t_id == "4":
            assert "⚙" in source, f"Unicode decoding failed for ID 4. Expected '⚙' in source, got: {source}"

        expected_conf = expected_confidences.get(t_id)
        assert expected_conf is not None, f"Unexpected ID found: {t_id}"
        assert abs(conf - expected_conf) <= 0.001, f"Incorrect confidence for ID {t_id}. Expected {expected_conf}, got {conf}"