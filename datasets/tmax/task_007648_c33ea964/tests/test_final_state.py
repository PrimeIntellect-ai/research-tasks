# test_final_state.py

import os
import csv
import unicodedata
import pytest

OUTPUT_CSV = "/home/user/output/clean_translations.csv"
RUN_SCRIPT = "/home/user/run.sh"
GO_CODE = "/home/user/loc_pipeline/process.go"

def test_files_exist():
    assert os.path.isfile(RUN_SCRIPT), f"Run script missing at {RUN_SCRIPT}"
    assert os.path.isfile(GO_CODE), f"Go source missing at {GO_CODE}"
    assert os.path.isfile(OUTPUT_CSV), f"Output file missing at {OUTPUT_CSV}"

def test_output_csv_content():
    if not os.path.isfile(OUTPUT_CSV):
        pytest.fail(f"Cannot check content, {OUTPUT_CSV} is missing.")

    with open(OUTPUT_CSV, "r", encoding="utf-8", newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 5, f"Expected 5 rows in the output CSV, but got {len(rows)}. Deduplication or processing might be incorrect."

    # Header
    assert rows[0] == ["EntryID", "Context", "SourceText", "Translation"], "Header row is incorrect or missing."

    # Row 1: Standard row
    assert rows[1] == ["1", "ui.button", "Save", "Enregistrer"], "First data row is incorrect."

    # Row 2: Embedded \r\n converted to \n
    assert rows[2] == ["2", "ui.alert", "Error occurred.\nPlease retry.", "Erreur.\nRéessayer."], "Embedded carriage returns were not correctly converted to standard newlines."

    # Row 3: Invalid UTF-8 replaced with U+FFFD
    assert rows[3][0] == "4"
    assert rows[3][1] == "ui.msg"
    assert "\ufffd" in rows[3][2], "Invalid UTF-8 byte sequence was not replaced with the Unicode Replacement Character (U+FFFD)."
    assert rows[3][3] == "Mauvais encodage"

    # Row 4: Unnormalized Unicode converted to NFC
    nfc_cafe = unicodedata.normalize('NFC', "Cafe\u0301")
    assert rows[4] == ["5", "ui.cafe", nfc_cafe, "Cafeteria"], "Unicode text was not correctly normalized to NFC."