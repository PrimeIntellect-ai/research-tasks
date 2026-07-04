# test_final_state.py
import socket
import json
import sqlite3
import pytest
import time

def test_tcp_server_response():
    """Connect to the TCP server, send REPORT, and validate the JSON response."""
    host = '127.0.0.1'
    port = 8000

    # Try connecting a few times in case the server is slow to start
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((host, port))
    except Exception as e:
        pytest.fail(f"Could not connect to TCP server at {host}:{port}: {e}")

    try:
        s.sendall(b"REPORT\n")
        response_data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response_data += chunk
    except Exception as e:
        pytest.fail(f"Error communicating with TCP server: {e}")
    finally:
        s.close()

    assert response_data, "Server returned an empty response."

    try:
        results = json.loads(response_data.decode('utf-8'))
    except json.JSONDecodeError as e:
        pytest.fail(f"Server response is not valid JSON: {e}\nResponse was: {response_data}")

    assert isinstance(results, list), "JSON response must be an array."
    assert len(results) == 10, f"Expected 10 frames in the result, got {len(results)}."

    # Extract raw brightness to verify smoothed calculations
    raw_brightness_list = []
    for i, row in enumerate(results):
        assert "frame" in row, f"Missing 'frame' in row {i}"
        assert "raw_brightness" in row, f"Missing 'raw_brightness' in row {i}"
        assert "smoothed_brightness" in row, f"Missing 'smoothed_brightness' in row {i}"
        assert "signal_name" in row, f"Missing 'signal_name' in row {i}"

        assert row["frame"] == i + 1, f"Expected frame {i+1}, got {row['frame']}"
        raw_brightness_list.append(row["raw_brightness"])

    # Verify smoothed logic and signal mapping
    for i, row in enumerate(results):
        # Calculate expected smoothed brightness
        window = []
        if i > 0:
            window.append(raw_brightness_list[i-1])
        window.append(raw_brightness_list[i])
        if i < len(raw_brightness_list) - 1:
            window.append(raw_brightness_list[i+1])

        expected_smoothed = round(sum(window) / len(window), 2)
        # Allow small floating point differences
        assert abs(row["smoothed_brightness"] - expected_smoothed) <= 0.02, \
            f"Frame {row['frame']}: expected smoothed_brightness ~{expected_smoothed}, got {row['smoothed_brightness']}"

        # Verify signal_name mapping
        sb = row["smoothed_brightness"]
        if 0.0 <= sb <= 50.0:
            expected_signal = "background"
        elif 50.01 <= sb <= 150.0:
            expected_signal = "low_activity"
        elif 150.01 <= sb <= 255.0:
            expected_signal = "high_activity"
        else:
            expected_signal = "unknown"

        assert row["signal_name"] == expected_signal, \
            f"Frame {row['frame']}: expected signal_name '{expected_signal}' for smoothed brightness {sb}, got '{row['signal_name']}'"

def test_database_table_exists():
    """Verify that the frame_data table was created and populated in reference.db."""
    db_path = "/app/reference.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='frame_data';")
        table = cursor.fetchone()
        assert table is not None, "Table 'frame_data' does not exist in /app/reference.db."

        # Check row count
        cursor.execute("SELECT COUNT(*) FROM frame_data;")
        count = cursor.fetchone()[0]
        assert count == 10, f"Expected 10 rows in frame_data, got {count}."

        # Check schema
        cursor.execute("PRAGMA table_info(frame_data);")
        columns = [col[1] for col in cursor.fetchall()]
        assert "frame" in columns or "frame_number" in columns or any("frame" in c.lower() for c in columns), "frame_data table missing a frame column."
        assert "raw_brightness" in columns or "brightness" in columns or any("bright" in c.lower() for c in columns), "frame_data table missing a brightness column."

    except sqlite3.Error as e:
        pytest.fail(f"SQLite error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()