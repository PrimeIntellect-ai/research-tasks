# test_final_state.py

import json
import difflib
import os
import pytest

def test_final_artifacts_json_and_transcription():
    output_path = '/home/user/final_artifacts.json'
    assert os.path.isfile(output_path), f"Final output file missing: {output_path}"

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File is not valid JSON: {output_path}")

    assert isinstance(data, list), "Output JSON must be an array of objects."

    transcription = None
    for item in data:
        if isinstance(item, dict) and item.get("id") == "release_notes":
            transcription = item.get("transcription")
            break

    assert transcription is not None, "Could not find 'release_notes' artifact with a 'transcription' field."
    assert isinstance(transcription, str), "'transcription' field must be a string."

    ground_truth = "Fixed the concurrent modification bug in the build cache and upgraded the networking library to version two point one."

    # Normalize
    t_norm = transcription.lower().strip()
    g_norm = ground_truth.lower().strip()

    similarity = difflib.SequenceMatcher(None, t_norm, g_norm).ratio()
    assert similarity >= 0.85, (
        f"Transcription similarity {similarity:.3f} is below the 0.85 threshold.\n"
        f"Expected (normalized): '{g_norm}'\n"
        f"Got (normalized): '{t_norm}'"
    )