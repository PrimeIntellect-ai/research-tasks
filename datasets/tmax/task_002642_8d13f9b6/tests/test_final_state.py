# test_final_state.py
import os
import csv

def get_original_data():
    return [
        {"key": "greeting", "en": "Hello", "fr": "Bonjour", "de": "Hallo", "es": "Hola"},
        {"key": "goodbye", "en": "Goodbye", "fr": "Au revoir", "de": "Auf Wiedersehen", "es": "Adiós"},
        {"key": "error_1", "en": "An unexpected error occurred.", "fr": "Une erreur inattendue s'est produite.", "de": "Ein unerwarteter Fehler ist aufgetreten.", "es": "Un error inesperado ha ocurrido."},
        {"key": "short_test", "en": "Yes", "fr": "Oui", "de": "Ja", "es": "Sí"},
        {"key": "anomaly_test", "en": "This is a normal sentence.", "fr": "C'est une phrase normale.", "de": "Dies ist ein normaler Satz.", "es": "X"},
        {"key": "long_anomaly", "en": "Short", "fr": "Ceci est une traduction française extrêmement longue qui ne correspond pas du tout au texte d'origine.", "de": "Kurz", "es": "Corto"},
        {"key": "btn_ok", "en": "OK", "fr": "OK", "de": "OK", "es": "OK"},
        {"key": "btn_cancel", "en": "Cancel", "fr": "Annuler", "de": "Abbrechen", "es": "Cancelar"}
    ]

def test_script_exists_and_executable():
    script_path = "/home/user/process_loc.sh"
    assert os.path.exists(script_path), f"Script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_long_format_csv():
    file_path = "/home/user/long_format.csv"
    assert os.path.exists(file_path), f"Missing {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, f"{file_path} is empty"
    assert reader[0] == ["key", "locale", "translation"], f"Incorrect header in {file_path}"

    expected_rows = []
    for row in get_original_data():
        key = row["key"]
        for loc in ["en", "fr", "de", "es"]:
            expected_rows.append([key, loc, row[loc]])

    # We check if the data matches the expected long format (ignoring row order)
    actual_data = reader[1:]
    assert len(actual_data) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(actual_data)}"

    for row in expected_rows:
        assert row in actual_data, f"Missing expected row {row} in {file_path}"

def test_anomalies_csv():
    file_path = "/home/user/anomalies.csv"
    assert os.path.exists(file_path), f"Missing {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, f"{file_path} is empty"
    assert reader[0] == ["key", "locale", "en_length", "trans_length"], f"Incorrect header in {file_path}"

    expected_anomalies = []
    for row in get_original_data():
        key = row["key"]
        en_len = len(row["en"])
        for loc in ["fr", "de", "es"]:
            trans_len = len(row[loc])
            if trans_len < 0.3 * en_len or trans_len > 3.0 * en_len:
                expected_anomalies.append([key, loc, str(en_len), str(trans_len)])

    actual_data = reader[1:]
    assert len(actual_data) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, got {len(actual_data)}"

    for row in expected_anomalies:
        assert row in actual_data, f"Missing expected anomaly {row} in {file_path}"

def test_sample_csv():
    file_path = "/home/user/sample.csv"
    assert os.path.exists(file_path), f"Missing {file_path}"

    with open(file_path, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, f"{file_path} is empty"
    assert reader[0] == ["key", "locale", "translation"], f"Incorrect header in {file_path}"

    # Compute expected sample
    original_data = get_original_data()
    sorted_keys = sorted([row["key"] for row in original_data])
    top_2_keys = sorted_keys[:2]

    expected_sample = []
    for loc in ["de", "en", "es", "fr"]: # sorted locales
        for key in top_2_keys: # sorted keys
            trans = next(r[loc] for r in original_data if r["key"] == key)
            expected_sample.append([key, loc, trans])

    actual_data = reader[1:]
    assert len(actual_data) == len(expected_sample), f"Expected {len(expected_sample)} sample rows, got {len(actual_data)}"
    assert actual_data == expected_sample, f"Sample data is incorrect or not sorted correctly. Expected: {expected_sample}, Got: {actual_data}"