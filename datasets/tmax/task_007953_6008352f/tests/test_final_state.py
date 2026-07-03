# test_final_state.py

import os
import csv
from datetime import datetime, timezone

def parse_timestamp(ts_str):
    try:
        return int(ts_str)
    except ValueError:
        dt = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
        dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())

def compute_expected_data(raw_file_path):
    if not os.path.exists(raw_file_path):
        return None

    records = []
    with open(raw_file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 4:
                continue
            string_id, ts_str, conf_str, locale = parts
            ts = parse_timestamp(ts_str)
            conf = float(conf_str)
            records.append({
                "string_id": string_id,
                "ts": ts,
                "conf": conf,
                "locale": locale
            })

    total_raw = len(records)

    # Deduplicate
    # Group by (StringID, Locale)
    # Keep max timestamp, if tie keep first seen
    groups = {}
    for rec in records:
        key = (rec["string_id"], rec["locale"])
        if key not in groups:
            groups[key] = rec
        else:
            if rec["ts"] > groups[key]["ts"]:
                groups[key] = rec

    deduped = list(groups.values())
    total_dedup = len(deduped)

    if total_dedup > 0:
        min_conf = min(r["conf"] for r in deduped)
        max_conf = max(r["conf"] for r in deduped)
    else:
        min_conf = 0.0
        max_conf = 0.0

    for r in deduped:
        if max_conf > min_conf:
            r["norm_conf"] = (r["conf"] - min_conf) / (max_conf - min_conf)
        else:
            r["norm_conf"] = 0.0

    deduped.sort(key=lambda x: (x["string_id"], x["locale"]))

    return {
        "total_raw": total_raw,
        "total_dedup": total_dedup,
        "min_conf": min_conf,
        "max_conf": max_conf,
        "records": deduped
    }

def test_processed_csv_exists_and_correct():
    csv_path = "/home/user/loc_data/processed.csv"
    raw_path = "/home/user/loc_data/raw_translations.txt"

    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."

    expected = compute_expected_data(raw_path)
    assert expected is not None, f"Input file {raw_path} is missing."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."
    header = rows[0]
    expected_header = ["StringID", "Locale", "UnixTimestamp", "NormalizedConfidence"]
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == len(expected["records"]), f"Expected {len(expected['records'])} data rows, got {len(data_rows)}."

    for i, (actual_row, exp_rec) in enumerate(zip(data_rows, expected["records"])):
        assert len(actual_row) == 4, f"Row {i+1} does not have 4 columns."
        assert actual_row[0] == exp_rec["string_id"], f"Row {i+1} StringID mismatch."
        assert actual_row[1] == exp_rec["locale"], f"Row {i+1} Locale mismatch."
        assert int(actual_row[2]) == exp_rec["ts"], f"Row {i+1} UnixTimestamp mismatch."
        assert f"{float(actual_row[3]):.4f}" == f"{exp_rec['norm_conf']:.4f}", f"Row {i+1} NormalizedConfidence mismatch."

def test_pipeline_log_exists_and_correct():
    log_path = "/home/user/loc_data/pipeline.log"
    raw_path = "/home/user/loc_data/raw_translations.txt"

    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    expected = compute_expected_data(raw_path)
    assert expected is not None, f"Input file {raw_path} is missing."

    with open(log_path, "r") as f:
        log_content = f.read().strip().split("\n")

    log_dict = {}
    for line in log_content:
        if ":" in line:
            k, v = line.split(":", 1)
            log_dict[k.strip()] = v.strip()

    assert "TOTAL_RAW" in log_dict, "TOTAL_RAW missing from log."
    assert int(log_dict["TOTAL_RAW"]) == expected["total_raw"], "TOTAL_RAW value is incorrect."

    assert "TOTAL_DEDUPLICATED" in log_dict, "TOTAL_DEDUPLICATED missing from log."
    assert int(log_dict["TOTAL_DEDUPLICATED"]) == expected["total_dedup"], "TOTAL_DEDUPLICATED value is incorrect."

    assert "MIN_CONF" in log_dict, "MIN_CONF missing from log."
    assert f"{float(log_dict['MIN_CONF']):.2f}" == f"{expected['min_conf']:.2f}", "MIN_CONF value is incorrect."

    assert "MAX_CONF" in log_dict, "MAX_CONF missing from log."
    assert f"{float(log_dict['MAX_CONF']):.2f}" == f"{expected['max_conf']:.2f}", "MAX_CONF value is incorrect."