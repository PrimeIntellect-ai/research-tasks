# test_final_state.py

import os
import sys
import json
import importlib.util
import pytest

EVIL_CORPUS_DIR = "/app/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
SANITIZER_MODULE_PATH = "/home/user/pipeline/sanitizer.py"
OUTPUT_JSON_PATH = "/home/user/pipeline/output.json"

def load_sanitizer():
    assert os.path.isfile(SANITIZER_MODULE_PATH), f"Sanitizer module not found at {SANITIZER_MODULE_PATH}"
    spec = importlib.util.spec_from_file_location("sanitizer", SANITIZER_MODULE_PATH)
    sanitizer = importlib.util.module_from_spec(spec)
    sys.modules["sanitizer"] = sanitizer
    try:
        spec.loader.exec_module(sanitizer)
    except Exception as e:
        pytest.fail(f"Failed to load sanitizer module: {e}")
    assert hasattr(sanitizer, "sanitize_text"), "sanitizer.py is missing 'sanitize_text' function."
    return sanitizer.sanitize_text

def test_sanitizer_clean_corpus():
    sanitize_text = load_sanitizer()
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.txt')]
    assert len(clean_files) > 0, "Clean corpus is empty."

    modified_clean = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        output = sanitize_text(content)
        if output != content:
            modified_clean.append(filename)

    if modified_clean:
        pytest.fail(f"{len(modified_clean)} of {len(clean_files)} clean files modified. Offending files: {', '.join(modified_clean[:5])}")

def test_sanitizer_evil_corpus():
    sanitize_text = load_sanitizer()
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.txt')]
    assert len(evil_files) > 0, "Evil corpus is empty."

    bypassed_evil = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        output = sanitize_text(content)
        if output == content or "[REDACTED]" not in output:
            bypassed_evil.append(filename)

    if bypassed_evil:
        pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed. Offending files: {', '.join(bypassed_evil[:5])}")

def test_output_json_structure_and_values():
    assert os.path.isfile(OUTPUT_JSON_PATH), f"Output JSON not found at {OUTPUT_JSON_PATH}"

    with open(OUTPUT_JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON_PATH} is not valid JSON.")

    assert isinstance(data, list), "Output JSON must be a list of objects."
    assert len(data) >= 3, "Output JSON must contain at least 3 segments from the audio."

    # Check schema for first item
    first_item = data[0]
    expected_keys = {"timestamp", "speaker_id", "original_length", "sanitized_text", "rolling_redaction_avg"}
    assert expected_keys.issubset(first_item.keys()), f"JSON objects missing required keys. Expected: {expected_keys}"

    # Check specific redaction logic and rolling averages based on truth
    # The truth expects rolling averages around 0.0, 0.33, 0.33 for the first 3 segments
    rolling_avgs = [item.get("rolling_redaction_avg", 0.0) for item in data[:3]]

    # We allow some float tolerance
    assert abs(rolling_avgs[0] - 0.0) < 0.01, f"Expected first rolling average to be 0.0, got {rolling_avgs[0]}"
    assert abs(rolling_avgs[1] - 0.33) < 0.05, f"Expected second rolling average to be ~0.33, got {rolling_avgs[1]}"
    assert abs(rolling_avgs[2] - 0.33) < 0.05, f"Expected third rolling average to be ~0.33, got {rolling_avgs[2]}"

    # Check that the second segment contains [REDACTED]
    assert "[REDACTED]" in data[1].get("sanitized_text", ""), "Second segment should contain '[REDACTED]'."
    assert "[REDACTED]" not in data[0].get("sanitized_text", ""), "First segment should NOT contain '[REDACTED]'."
    assert "[REDACTED]" not in data[2].get("sanitized_text", ""), "Third segment should NOT contain '[REDACTED]'."