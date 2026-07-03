# test_final_state.py
import os
import json
import math
import wave
import struct
import sqlite3

def test_output_mse():
    """
    Validates that the output.json exists and its computed RMS values
    have an MSE < 0.001 compared to the ground truth.
    """
    output_path = '/app/output.json'
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        try:
            output = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Failed to parse {output_path} as JSON."

    # Read the audio samples to compute ground truth
    wav_path = '/app/data.wav'
    assert os.path.exists(wav_path), f"Audio file {wav_path} is missing."

    with wave.open(wav_path, 'r') as wav:
        frames = wav.readframes(wav.getnframes())
        samples = struct.unpack(f"{len(frames)//2}h", frames)

    # Read the events from the database
    db_path = '/app/events.db'
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT event_id, start_sample, end_sample FROM events')
    events = c.fetchall()
    conn.close()

    assert len(events) > 0, "No events found in the database."

    # Compute ground truth RMS for each event
    truth = {}
    for eid, start, end in events:
        chunk = samples[start:end]
        assert len(chunk) > 0, f"Event {eid} has an empty sample chunk."
        sq_sum = sum(x * x for x in chunk)
        truth[str(eid)] = math.sqrt(sq_sum / len(chunk))

    # Calculate Mean Squared Error
    mse = 0.0
    for eid, true_val in truth.items():
        assert eid in output, f"Event ID {eid} is missing from {output_path}."

        try:
            pred_val = float(output[eid])
        except (ValueError, TypeError):
            assert False, f"Value for event {eid} in {output_path} is not a valid float."

        mse += (pred_val - true_val) ** 2

    mse /= len(truth)

    # Assert against the threshold
    threshold = 0.001
    assert mse < threshold, f"MSE too high: {mse} >= {threshold}. The calculated RMS values are incorrect."