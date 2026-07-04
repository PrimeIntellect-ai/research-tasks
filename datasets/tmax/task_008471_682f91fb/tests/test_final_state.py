# test_final_state.py

import os
import subprocess
import xml.etree.ElementTree as ET
import pytest

def test_crontab_configured():
    try:
        cron_out = subprocess.check_output(["crontab", "-l"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Ensure a crontab is installed for the user.")

    assert "0 2 * * *" in cron_out, "Crontab does not have the correct schedule (0 2 * * *)."
    assert "run_pipeline.sh" in cron_out, "Crontab does not execute run_pipeline.sh."

def test_processed_files_exist():
    expected_files = [
        "/home/user/processed/2023-11-01/lang_fr-FR.csv",
        "/home/user/processed/2023-11-01/lang_fr-FR.xml",
        "/home/user/processed/2023-11-01/lang_fr-FR.parquet",
        "/home/user/processed/2023-11-01/lang_es-ES.csv",
        "/home/user/processed/2023-11-01/lang_es-ES.xml",
        "/home/user/processed/2023-11-01/lang_es-ES.parquet",
        "/home/user/processed/2023-11-02/lang_fr-FR.csv",
        "/home/user/processed/2023-11-02/lang_fr-FR.xml",
        "/home/user/processed/2023-11-02/lang_fr-FR.parquet",
        "/home/user/processed/2023-11-02/lang_es-ES.csv",
        "/home/user/processed/2023-11-02/lang_es-ES.xml",
        "/home/user/processed/2023-11-02/lang_es-ES.parquet",
    ]

    for file_path in expected_files:
        assert os.path.exists(file_path), f"Expected output file missing: {file_path}"

def test_data_cleaning_csv():
    fr_csv = "/home/user/processed/2023-11-01/lang_fr-FR.csv"
    assert os.path.exists(fr_csv), f"Missing {fr_csv}"
    with open(fr_csv, "r", encoding="utf-8") as f:
        content = f.read()
        assert "[ERR]" in content, f"Expected invalid unicode to be replaced with [ERR] in {fr_csv}"
        assert "ZZZZ" not in content, f"Invalid unicode sequence ZZZZ was not removed in {fr_csv}"

    es_csv = "/home/user/processed/2023-11-02/lang_es-ES.csv"
    assert os.path.exists(es_csv), f"Missing {es_csv}"
    with open(es_csv, "r", encoding="utf-8") as f:
        content = f.read()
        assert "[ERR]" in content, f"Expected invalid unicode to be replaced with [ERR] in {es_csv}"
        assert "12XY" not in content, f"Invalid unicode sequence 12XY was not removed in {es_csv}"

def test_xml_structure():
    es_xml = "/home/user/processed/2023-11-01/lang_es-ES.xml"
    assert os.path.exists(es_xml), f"Missing {es_xml}"

    try:
        tree = ET.parse(es_xml)
        root = tree.getroot()
    except ET.ParseError:
        pytest.fail(f"Failed to parse XML file: {es_xml}")

    assert root.tag == "resources", "XML root element must be <resources>"
    assert len(root) > 0, "XML <resources> element is empty"

    # Find the welcome string
    welcome_element = None
    for child in root:
        if child.tag == "string" and child.attrib.get("name") == "welcome":
            welcome_element = child
            break

    assert welcome_element is not None, "Could not find <string name=\"welcome\"> in XML"
    assert welcome_element.text == "Hola !", f"Expected 'Hola !', got '{welcome_element.text}'"

def test_parquet_format():
    fr_parquet = "/home/user/processed/2023-11-01/lang_fr-FR.parquet"
    assert os.path.exists(fr_parquet), f"Missing {fr_parquet}"

    # Since we can only use stdlib, we verify the Parquet magic bytes
    with open(fr_parquet, "rb") as f:
        magic = f.read(4)
        assert magic == b"PAR1", f"File {fr_parquet} does not appear to be a valid Parquet file (missing PAR1 magic bytes)"