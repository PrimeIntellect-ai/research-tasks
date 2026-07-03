# test_final_state.py

import os
import sys
import glob
import json
import difflib
import pytest

# Ensure we can import the vendored polib package
sys.path.insert(0, '/app/vendored/polib-1.1.1')
try:
    import polib
except ImportError:
    pytest.fail("Could not import polib from /app/vendored/polib-1.1.1")

def test_fixed_locales_accuracy():
    golden_files = glob.glob('/app/golden_locales/*.po')
    assert len(golden_files) > 0, "No golden locale files found in /app/golden_locales"

    total_ratio = 0.0
    count = 0

    for golden_path in golden_files:
        lang = os.path.basename(golden_path)
        agent_path = f'/home/user/fixed_locales/{lang}'

        assert os.path.exists(agent_path), f"Missing fixed locale file: {agent_path}"

        golden_po = polib.pofile(golden_path, encoding='utf-8')
        try:
            agent_po = polib.pofile(agent_path, encoding='utf-8')
        except Exception as e:
            pytest.fail(f"Failed to parse agent's fixed file {agent_path}: {e}")

        assert len(golden_po) == len(agent_po), f"Mismatch in number of entries for {lang}"

        for g_entry, a_entry in zip(golden_po, agent_po):
            ratio = difflib.SequenceMatcher(None, g_entry.msgstr, a_entry.msgstr).ratio()
            total_ratio += ratio
            count += 1

    avg_accuracy = total_ratio / count if count > 0 else 0
    assert avg_accuracy >= 0.98, f"Character-level accuracy {avg_accuracy:.4f} is below the required threshold of 0.98"

def test_summary_json():
    summary_path = '/home/user/summary.json'
    assert os.path.exists(summary_path), f"Missing summary statistics file: {summary_path}"

    with open(summary_path, 'r', encoding='utf-8') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON")

    golden_files = glob.glob('/app/golden_locales/*.po')

    for golden_path in golden_files:
        lang_key = os.path.basename(golden_path).replace('.po', '')
        assert lang_key in summary, f"Language '{lang_key}' is missing from {summary_path}"

        golden_po = polib.pofile(golden_path, encoding='utf-8')
        non_empty_entries = [e for e in golden_po if e.msgstr]

        expected_total = len(non_empty_entries)
        if expected_total > 0:
            expected_avg = round(sum(len(e.msgstr) for e in non_empty_entries) / expected_total, 2)
        else:
            expected_avg = 0.0

        agent_total = summary[lang_key].get('total_translations')
        agent_avg = summary[lang_key].get('avg_translation_length')

        assert agent_total is not None, f"Missing 'total_translations' for {lang_key}"
        assert agent_avg is not None, f"Missing 'avg_translation_length' for {lang_key}"

        assert agent_total == expected_total, f"Expected total_translations={expected_total} for {lang_key}, got {agent_total}"
        assert abs(agent_avg - expected_avg) <= 0.01, f"Expected avg_translation_length~={expected_avg} for {lang_key}, got {agent_avg}"