# test_final_state.py

import os
import json
import xml.etree.ElementTree as ET
import subprocess
import pytest

INCOMING_DIR = "/home/user/data/incoming"
ARCHIVE_DIR = "/home/user/data/archive"
OUTPUT_JSON = "/home/user/data/output/metrics.json"
OUTPUT_XML = "/home/user/data/output/metrics.xml"

EXPECTED_METRICS = {
    "e1": {"device_id": "devA", "sensor_value": 10.0, "rolling_avg": 10.0},
    "e2": {"device_id": "devB", "sensor_value": 20.0, "rolling_avg": 20.0},
    "e3": {"device_id": "devA", "sensor_value": 15.0, "rolling_avg": 12.5},
    "e4": {"device_id": "devA", "sensor_value": 20.0, "rolling_avg": 15.0},
    "e5": {"device_id": "devA", "sensor_value": 25.0, "rolling_avg": 20.0},
    "e6": {"device_id": "devB", "sensor_value": 30.0, "rolling_avg": 25.0},
    "e7": {"device_id": "devB", "sensor_value": 40.0, "rolling_avg": 30.0},
}

def test_incoming_directory_empty():
    """Verify that the incoming directory is empty after processing."""
    assert os.path.isdir(INCOMING_DIR), f"Directory missing: {INCOMING_DIR}"
    files = os.listdir(INCOMING_DIR)
    csv_files = [f for f in files if f.endswith('.csv')]
    assert len(csv_files) == 0, f"Incoming directory is not empty, found: {csv_files}"

def test_archive_directory_contains_files():
    """Verify that processed files were moved to the archive directory."""
    assert os.path.isdir(ARCHIVE_DIR), f"Directory missing: {ARCHIVE_DIR}"
    files = os.listdir(ARCHIVE_DIR)
    assert "batch1.csv" in files, "batch1.csv is missing from the archive directory"
    assert "batch2.csv" in files, "batch2.csv is missing from the archive directory"

def test_json_output():
    """Verify the JSON output format and correctness of calculations."""
    assert os.path.isfile(OUTPUT_JSON), f"JSON output file missing: {OUTPUT_JSON}"

    with open(OUTPUT_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not valid JSON")

    assert isinstance(data, list), "JSON root must be an array"
    assert len(data) == 7, f"Expected 7 records in JSON, found {len(data)}"

    for record in data:
        event_id = record.get("event_id")
        assert event_id in EXPECTED_METRICS, f"Unexpected event_id in JSON: {event_id}"
        expected = EXPECTED_METRICS[event_id]

        assert record.get("device_id") == expected["device_id"], f"Incorrect device_id for {event_id}"
        assert float(record.get("sensor_value")) == expected["sensor_value"], f"Incorrect sensor_value for {event_id}"
        assert float(record.get("rolling_avg")) == expected["rolling_avg"], f"Incorrect rolling_avg for {event_id}"

def test_xml_output():
    """Verify the XML output format and correctness of calculations."""
    assert os.path.isfile(OUTPUT_XML), f"XML output file missing: {OUTPUT_XML}"

    try:
        tree = ET.parse(OUTPUT_XML)
        root = tree.getroot()
    except ET.ParseError:
        pytest.fail("metrics.xml is not valid XML")

    assert root.tag == "metrics", "XML root element must be <metrics>"

    metrics = root.findall("metric")
    assert len(metrics) == 7, f"Expected 7 <metric> elements in XML, found {len(metrics)}"

    for metric in metrics:
        event_id = metric.findtext("event_id")
        assert event_id in EXPECTED_METRICS, f"Unexpected event_id in XML: {event_id}"
        expected = EXPECTED_METRICS[event_id]

        assert metric.findtext("device_id") == expected["device_id"], f"Incorrect device_id for {event_id}"
        assert float(metric.findtext("sensor_value")) == expected["sensor_value"], f"Incorrect sensor_value for {event_id}"
        assert float(metric.findtext("rolling_avg")) == expected["rolling_avg"], f"Incorrect rolling_avg for {event_id}"

def test_cron_job_scheduled():
    """Verify that a cron job is scheduled to run every 5 minutes."""
    try:
        result = subprocess.run(
            ["crontab", "-l"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab or no crontab exists for the user.")

    # Check for */5 in the crontab output
    valid_cron_found = any(
        line.strip() and not line.strip().startswith("#") and ("*/5" in line.split()[0] or "0,5,10,15,20,25,30,35,40,45,50,55" in line.split()[0])
        for line in crontab_output.splitlines()
    )

    assert valid_cron_found, "Could not find a cron job scheduled to run every 5 minutes (*/5) in the user's crontab."