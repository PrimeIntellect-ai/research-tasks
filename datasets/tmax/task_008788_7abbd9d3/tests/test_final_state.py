# test_final_state.py

import os
import csv
import pytest

def test_wide_locales_exists_and_format():
    """Verify that wide_locales.csv exists and has the correct columns and sorting."""
    file_path = '/home/user/wide_locales.csv'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers is not None, "wide_locales.csv is empty."
        assert headers[0] == 'msg_id', "First column must be 'msg_id'."

        locales = headers[1:]
        assert locales == sorted(locales), "Locale columns must be sorted alphabetically."
        assert 'en' in locales, "'en' locale column is missing."
        assert 'es' in locales, "'es' locale column is missing."

        rows = list(reader)
        msg_ids = [row[0] for row in rows]
        assert msg_ids == sorted(msg_ids), "Rows must be sorted alphabetically by msg_id."

def test_wide_locales_content():
    """Verify the deduplication and reshaping logic in wide_locales.csv."""
    file_path = '/home/user/wide_locales.csv'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        # Check specific rows based on the truth data
        msg_dict = {row['msg_id']: row for row in rows}

        # 'farewell' should have 'Goodbye' and 'Adiós' (latest timestamp)
        assert 'farewell' in msg_dict, "'farewell' msg_id is missing."
        assert msg_dict['farewell']['en'] == 'Goodbye'
        assert msg_dict['farewell']['es'] == 'Adiós', "Latest timestamp deduplication failed for 'farewell'."

        # 'greeting' should have embedded newlines correctly preserved
        assert 'greeting' in msg_dict, "'greeting' msg_id is missing."
        assert msg_dict['greeting']['en'] == 'Hello\nWorld', "Embedded newlines not preserved for 'greeting' en."
        assert msg_dict['greeting']['es'] == 'Hola\nMundo', "Embedded newlines not preserved for 'greeting' es."

        # 'test1' should be present
        assert 'test1' in msg_dict, "'test1' msg_id is missing."
        assert msg_dict['test1']['en'] == 'Test'
        assert msg_dict['test1']['es'] == 'Prueba'

        # 'test2' should be dropped because its 'en' translation is identical to 'test1'
        # ('test1' < 'test2' lexicographically)
        assert 'test2' not in msg_dict, "'test2' should have been dropped due to hash-based deduplication."

        # 'orphan' should be dropped because it lacks an 'en' translation
        assert 'orphan' not in msg_dict, "'orphan' should have been dropped because it lacks an 'en' translation."

def test_reports_generated():
    """Verify that the month bucket reports are generated correctly."""
    report_10 = '/home/user/report_2023-10.txt'
    report_11 = '/home/user/report_2023-11.txt'
    report_12 = '/home/user/report_2023-12.txt'

    assert os.path.isfile(report_10), f"Report {report_10} is missing."
    with open(report_10, 'r') as f:
        content = f.read()
        assert 'Month: 2023-10' in content
        assert 'Messages: 2' in content, f"Expected 2 messages in {report_10}"

    assert os.path.isfile(report_11), f"Report {report_11} is missing."
    with open(report_11, 'r') as f:
        content = f.read()
        assert 'Month: 2023-11' in content
        assert 'Messages: 1' in content, f"Expected 1 message in {report_11}"

    assert not os.path.exists(report_12), f"Report {report_12} should not exist ('orphan' was dropped)."