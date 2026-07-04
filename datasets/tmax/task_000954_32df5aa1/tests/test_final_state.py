# test_final_state.py
import os
import re

def test_etl_output_exists():
    assert os.path.isfile("/home/user/etl_output.sql"), "/home/user/etl_output.sql was not generated."

def test_etl_output_content():
    expected_statements = {
        "INSERT INTO bus_proximity (timestamp, bus_id, point_id, distance) VALUES ('2023-10-01T10:00:10Z', 'bus_1', 'point_A', 40.00);",
        "INSERT INTO bus_proximity (timestamp, bus_id, point_id, distance) VALUES ('2023-10-01T10:00:10Z', 'bus_1', 'point_B', 20.62);",
        "INSERT INTO bus_proximity (timestamp, bus_id, point_id, distance) VALUES ('2023-10-01T10:00:20Z', 'bus_1', 'point_A', 40.31);",
        "INSERT INTO bus_proximity (timestamp, bus_id, point_id, distance) VALUES ('2023-10-01T10:00:20Z', 'bus_1', 'point_B', 0.00);",
        "INSERT INTO bus_proximity (timestamp, bus_id, point_id, distance) VALUES ('2023-10-01T10:00:30Z', 'bus_1', 'point_A', 50.00);",
        "INSERT INTO bus_proximity (timestamp, bus_id, point_id, distance) VALUES ('2023-10-01T10:00:30Z', 'bus_1', 'point_B', 20.62);",
        "INSERT INTO bus_proximity (timestamp, bus_id, point_id, distance) VALUES ('2023-10-01T10:00:40Z', 'bus_1', 'point_B', 40.31);"
    }

    with open("/home/user/etl_output.sql", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_statements), f"Expected {len(expected_statements)} SQL statements, but found {len(lines)}."

    # Verify chronological ordering
    timestamps = []
    for line in lines:
        match = re.search(r"\('([^']+)'", line)
        assert match is not None, f"Could not parse timestamp from line: {line}"
        timestamps.append(match.group(1))

    assert timestamps == sorted(timestamps), "The SQL statements are not ordered chronologically."

    # Verify exact contents
    actual_statements = set(lines)
    missing = expected_statements - actual_statements
    extra = actual_statements - expected_statements

    error_msg = []
    if missing:
        error_msg.append(f"Missing expected statements:\n" + "\n".join(missing))
    if extra:
        error_msg.append(f"Unexpected statements found:\n" + "\n".join(extra))

    assert not missing and not extra, "\n".join(error_msg)