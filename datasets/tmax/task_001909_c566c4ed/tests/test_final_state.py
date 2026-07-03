# test_final_state.py

import os
import csv

def test_aggregated_loc_stats_csv_exists_and_correct():
    output_path = "/home/user/aggregated_loc_stats.csv"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

    expected_rows = [
        ["bucket_start_iso8601", "locale", "avg_render_time_ms"],
        ["2023-10-15T10:00:00Z", "de-DE", "0.0"],
        ["2023-10-15T10:00:00Z", "es-ES", "45.0"],
        ["2023-10-15T10:00:00Z", "fr-FR", "60.0"],
        ["2023-10-15T10:01:00Z", "de-DE", "0.0"],
        ["2023-10-15T10:01:00Z", "es-ES", "0.0"],
        ["2023-10-15T10:01:00Z", "fr-FR", "0.0"],
        ["2023-10-15T10:02:00Z", "de-DE", "100.0"],
        ["2023-10-15T10:02:00Z", "es-ES", "0.0"],
        ["2023-10-15T10:02:00Z", "fr-FR", "0.0"],
        ["2023-10-15T10:03:00Z", "de-DE", "0.0"],
        ["2023-10-15T10:03:00Z", "es-ES", "0.0"],
        ["2023-10-15T10:03:00Z", "fr-FR", "0.0"],
        ["2023-10-15T10:04:00Z", "de-DE", "0.0"],
        ["2023-10-15T10:04:00Z", "es-ES", "0.0"],
        ["2023-10-15T10:04:00Z", "fr-FR", "80.0"]
    ]

    actual_rows = []
    with open(output_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)} rows in {output_path}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i} mismatch. Expected {expected}, got {actual}."