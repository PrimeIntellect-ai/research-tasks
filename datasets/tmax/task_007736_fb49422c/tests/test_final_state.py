# test_final_state.py
import os
import json
import pytest

CLEAN_FILE = "/home/user/tickets_clean.jsonl"

@pytest.fixture
def clean_data():
    assert os.path.exists(CLEAN_FILE), f"The output file {CLEAN_FILE} does not exist."

    records = {}
    with open(CLEAN_FILE, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                pytest.fail(f"Failed to parse JSON on line {line_num} of {CLEAN_FILE}: {e}")

            assert "filename" in data, f"Record on line {line_num} is missing the 'filename' key."
            records[data["filename"]] = data

    return records

def test_output_file_exists_and_has_five_records(clean_data):
    """Test that the output JSONL file contains exactly 5 records."""
    assert len(clean_data) == 5, f"Expected 5 records in {CLEAN_FILE}, found {len(clean_data)}."

def test_record_keys(clean_data):
    """Test that each record has exactly the required keys."""
    expected_keys = {"date", "email", "error_code", "message", "filename"}
    for filename, record in clean_data.items():
        assert set(record.keys()) == expected_keys, f"Record for {filename} does not have the exact expected keys. Found: {set(record.keys())}"

def test_ticket_1_extraction(clean_data):
    """Test extraction for ticket_1.txt."""
    record = clean_data.get("ticket_1.txt")
    assert record is not None, "ticket_1.txt record not found."
    assert record["date"] == "2023-10-01"
    assert record["email"] == "alice@example.com"
    assert record["error_code"] == "ERR_404"
    assert "The requested file was not found." in record["message"]

def test_ticket_2_imputation_and_encoding(clean_data):
    """Test imputation and ISO-8859-1 decoding for ticket_2.txt."""
    record = clean_data.get("ticket_2.txt")
    assert record is not None, "ticket_2.txt record not found."
    assert record["date"] == "2023-10-02"
    assert record["email"] == "bob@test.org"
    assert record["error_code"] == "ERR_504", "Expected ERR_504 imputed from 'timeout'."
    assert "falló" in record["message"], "Special characters were not correctly decoded from ISO-8859-1."

def test_ticket_3_imputation_and_encoding(clean_data):
    """Test imputation and Windows-1252 decoding for ticket_3.txt."""
    record = clean_data.get("ticket_3.txt")
    assert record is not None, "ticket_3.txt record not found."
    assert record["date"] == "2023-10-03"
    assert record["email"] == "charlie@domain.net"
    assert record["error_code"] == "ERR_403", "Expected ERR_403 imputed from 'denied'."
    assert "€" in record["message"], "Special character '€' (\x80) was not correctly decoded from Windows-1252."

def test_ticket_4_imputation(clean_data):
    """Test imputation for ticket_4.txt (missing Error line completely)."""
    record = clean_data.get("ticket_4.txt")
    assert record is not None, "ticket_4.txt record not found."
    assert record["date"] == "2023-10-04"
    assert record["email"] == "dave@example.com"
    assert record["error_code"] == "ERR_500", "Expected ERR_500 imputed from 'exception'."

def test_ticket_5_imputation(clean_data):
    """Test imputation for ticket_5.txt (generic message)."""
    record = clean_data.get("ticket_5.txt")
    assert record is not None, "ticket_5.txt record not found."
    assert record["date"] == "2023-10-05"
    assert record["email"] == "eve@hacker.net"
    assert record["error_code"] == "ERR_UNKNOWN", "Expected ERR_UNKNOWN for generic message."