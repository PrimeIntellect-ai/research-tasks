# test_final_state.py

import os
import xml.etree.ElementTree as ET

def test_output_xml_exists():
    """Check if the output XML file exists."""
    file_path = "/home/user/locales/es_ES.xml"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

def test_output_xml_content():
    """Check if the output XML file contains the correctly processed data."""
    file_path = "/home/user/locales/es_ES.xml"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_content = """<locale>
  <string id="balance" notes="User query from ***@email.com">Your current balance is 127.50€.</string>
  <string id="fee" notes="Alert ***@fintech.net">A transaction fee of 1.28€ applies.</string>
  <string id="promo" notes="Approved by ***@promo.co.uk">Get 42.50€ off your next purchase of 170.00€!</string>
</locale>"""

    # We do a direct string comparison to ensure the exact format requested,
    # as the prompt specifies checking the structure and values including indentation.
    # However, to be robust against minor newline variations, we can split by lines and compare.

    actual_lines = [line.strip("\r\n") for line in content.splitlines()]
    expected_lines = [line.strip("\r\n") for line in expected_content.splitlines()]

    assert actual_lines == expected_lines, "The output XML content does not match the expected format or values."

def test_xml_is_valid():
    """Check if the output is valid XML and has correct structure."""
    file_path = "/home/user/locales/es_ES.xml"
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        assert False, f"Output file is not valid XML: {e}"

    assert root.tag == "locale", "Root element must be <locale>."

    strings = root.findall("string")
    assert len(strings) == 3, "There should be exactly 3 <string> elements."

    expected_data = [
        {"id": "balance", "notes": "User query from ***@email.com", "text": "Your current balance is 127.50€."},
        {"id": "fee", "notes": "Alert ***@fintech.net", "text": "A transaction fee of 1.28€ applies."},
        {"id": "promo", "notes": "Approved by ***@promo.co.uk", "text": "Get 42.50€ off your next purchase of 170.00€!"}
    ]

    for i, expected in enumerate(expected_data):
        assert strings[i].attrib.get("id") == expected["id"], f"Expected id '{expected['id']}'"
        assert strings[i].attrib.get("notes") == expected["notes"], f"Expected notes '{expected['notes']}'"
        assert strings[i].text == expected["text"], f"Expected text '{expected['text']}'"