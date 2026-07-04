# test_final_state.py
import os
import csv
import re
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_loc.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def process_data():
    en_path = "/home/user/loc_data/en_master.csv"
    fr_path = "/home/user/loc_data/fr_fr.txt"
    es_path = "/home/user/loc_data/es_es.txt"

    en_data = {}
    if os.path.exists(en_path):
        with open(en_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    en_data[row[0]] = row[1]

    fr_data = {}
    if os.path.exists(fr_path):
        with open(fr_path, "r", encoding="iso-8859-1") as f:
            for line in f:
                m = re.match(r'\[(.*?)\]\s*=\s*"(.*?)"', line.strip())
                if m:
                    fr_data[m.group(1)] = m.group(2)

    es_data = {}
    if os.path.exists(es_path):
        with open(es_path, "r", encoding="utf-16le") as f:
            for line in f:
                m = re.match(r'Key:\s*(.*?)\s*\|\s*Val:\s*"(.*?)"', line.strip())
                if m:
                    es_data[m.group(1)] = m.group(2)

    merged = []
    for key in sorted(en_data.keys()):
        en_val = en_data.get(key, "")
        fr_val = fr_data.get(key, "")
        es_val = es_data.get(key, "")
        merged.append((key, en_val, fr_val, es_val))

    stats = []
    lengths = []
    for row in merged:
        key, _, fr_val, es_val = row
        l = len(fr_val) + len(es_val)
        lengths.append(l)

        window = lengths[-3:]
        avg = sum(window) / len(window)
        stats.append((key, round(avg, 1)))

    return merged, stats

def test_merged_translations():
    out_path = "/home/user/output/merged_translations.csv"
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    expected_merged, _ = process_data()

    actual_merged = []
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            assert header == ["Key", "EN", "FR", "ES"], f"Incorrect header in {out_path}"
            for row in reader:
                actual_merged.append(tuple(row))
    except UnicodeDecodeError:
        pytest.fail(f"Output file {out_path} is not valid UTF-8.")

    assert actual_merged == expected_merged, "Merged translations do not match the expected output format or data."

def test_stats():
    out_path = "/home/user/output/stats.csv"
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    _, expected_stats = process_data()

    actual_stats = []
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            assert header == ["Key", "RollingAvg"], f"Incorrect header in {out_path}"
            for row in reader:
                if len(row) >= 2:
                    actual_stats.append((row[0], float(row[1])))
    except UnicodeDecodeError:
        pytest.fail(f"Output file {out_path} is not valid UTF-8.")
    except ValueError:
        pytest.fail(f"Output file {out_path} contains invalid numeric values for RollingAvg.")

    assert len(actual_stats) == len(expected_stats), "Stats row count mismatch."
    for actual, expected in zip(actual_stats, expected_stats):
        assert actual[0] == expected[0], f"Key mismatch in stats: {actual[0]} != {expected[0]}"
        assert abs(actual[1] - expected[1]) < 0.05, f"Rolling average mismatch for key {actual[0]}: expected {expected[1]}, got {actual[1]}"