# test_final_state.py

import os
import json
import pytest

OUTPUT_FILE = "/home/user/processed_translations.json"

@pytest.fixture
def processed_data():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file."

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file {OUTPUT_FILE} is not valid JSON: {e}")

    return data

def test_top_level_keys(processed_data):
    expected_locales = {"en-US", "fr-FR", "ar-SA"}
    actual_locales = set(processed_data.keys())
    assert actual_locales == expected_locales, f"Expected locales {expected_locales}, but got {actual_locales}."

def test_sorting_by_key(processed_data):
    for loc, items in processed_data.items():
        keys = [item.get("key") for item in items]
        assert keys == sorted(keys), f"Items for locale '{loc}' are not sorted alphabetically by key. Got: {keys}"

def test_imputation(processed_data):
    # fr-FR farewell
    fr_items = processed_data.get("fr-FR", [])
    fr_farewell = next((item for item in fr_items if item.get("key") == "farewell"), None)
    assert fr_farewell is not None, "Missing 'farewell' key in 'fr-FR' locale."
    assert fr_farewell.get("text") == "Goodbye 👋", "Imputation failed for fr-FR 'farewell'."

    # ar-SA items
    ar_items = processed_data.get("ar-SA", [])
    ar_items_obj = next((item for item in ar_items if item.get("key") == "items"), None)
    assert ar_items_obj is not None, "Missing 'items' key in 'ar-SA' locale."
    assert ar_items_obj.get("text") == "You have {count} items in your {container}.", "Imputation failed for ar-SA 'items'."

def test_features_extraction(processed_data):
    # en-US farewell
    en_items = processed_data.get("en-US", [])
    en_farewell = next((item for item in en_items if item.get("key") == "farewell"), None)
    assert en_farewell is not None, "Missing 'farewell' key in 'en-US' locale."

    features = en_farewell.get("features")
    assert features is not None, "Features object is missing for en-US 'farewell'."
    assert features.get("char_count") == 9, f"Expected char_count 9 for en-US 'farewell', got {features.get('char_count')}"
    assert features.get("placeholders") == 0, f"Expected placeholders 0 for en-US 'farewell', got {features.get('placeholders')}"

    # en-US welcome
    en_welcome = next((item for item in en_items if item.get("key") == "welcome"), None)
    assert en_welcome is not None, "Missing 'welcome' key in 'en-US' locale."
    features = en_welcome.get("features")
    assert features is not None, "Features object is missing for en-US 'welcome'."
    assert features.get("char_count") == 21, f"Expected char_count 21 for en-US 'welcome', got {features.get('char_count')}"
    assert features.get("placeholders") == 1, f"Expected placeholders 1 for en-US 'welcome', got {features.get('placeholders')}"

    # ar-SA welcome
    ar_items = processed_data.get("ar-SA", [])
    ar_welcome = next((item for item in ar_items if item.get("key") == "welcome"), None)
    assert ar_welcome is not None, "Missing 'welcome' key in 'ar-SA' locale."
    features = ar_welcome.get("features")
    assert features is not None, "Features object is missing for ar-SA 'welcome'."
    assert features.get("char_count") == 23, f"Expected char_count 23 for ar-SA 'welcome', got {features.get('char_count')}"
    assert features.get("placeholders") == 1, f"Expected placeholders 1 for ar-SA 'welcome', got {features.get('placeholders')}"

    # ar-SA items
    ar_items_obj = next((item for item in ar_items if item.get("key") == "items"), None)
    assert ar_items_obj is not None, "Missing 'items' key in 'ar-SA' locale."
    features = ar_items_obj.get("features")
    assert features is not None, "Features object is missing for ar-SA 'items'."
    assert features.get("char_count") == 39, f"Expected char_count 39 for ar-SA 'items', got {features.get('char_count')}"
    assert features.get("placeholders") == 2, f"Expected placeholders 2 for ar-SA 'items', got {features.get('placeholders')}"