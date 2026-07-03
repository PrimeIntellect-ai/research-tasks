# test_final_state.py

import os
import json
import pytest
import jiwer

def test_go_file_exists():
    """Check if the Go program was created at the correct path."""
    path = "/home/user/pipeline/process.go"
    assert os.path.isfile(path), f"The Go program is missing at {path}."

def test_summary_json_exists():
    """Check if the output JSON file exists."""
    path = "/home/user/pipeline/summary.json"
    assert os.path.isfile(path), f"The summary.json file is missing at {path}."

def test_wer_metric():
    """Verify that the Word Error Rate (WER) is within the acceptable threshold."""
    path = "/home/user/pipeline/summary.json"
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse summary.json: {e}")

    assert "speakers" in data, "The JSON must contain a 'speakers' key."

    ground_truth = {
        "Speaker_1": "we are here today to discuss the new automation pipeline that will be deployed next week.",
        "Speaker_2": "i have reviewed the initial design and the concurrency model looks solid."
    }

    total_wer = 0.0
    for speaker, truth_text in ground_truth.items():
        assert speaker in data["speakers"], f"Missing {speaker} in output JSON."

        hypothesis = data["speakers"][speaker].get("transcript", "").lower().strip()

        # Remove punctuation for fair comparison
        truth_clean = "".join(c for c in truth_text if c.isalnum() or c.isspace())
        hyp_clean = "".join(c for c in hypothesis if c.isalnum() or c.isspace())

        # Normalize spaces
        truth_clean = " ".join(truth_clean.split())
        hyp_clean = " ".join(hyp_clean.split())

        error_rate = jiwer.wer(truth_clean, hyp_clean)
        total_wer += error_rate

    avg_wer = total_wer / len(ground_truth)
    assert avg_wer <= 0.20, f"Average WER too high: {avg_wer:.4f} > 0.20 threshold."

def test_word_count_matches_transcript():
    """Verify that the word count matches the number of words in the transcript."""
    path = "/home/user/pipeline/summary.json"
    with open(path, "r") as f:
        data = json.load(f)

    for speaker, info in data.get("speakers", {}).items():
        assert "transcript" in info, f"Missing 'transcript' for {speaker}."
        assert "word_count" in info, f"Missing 'word_count' for {speaker}."

        transcript = info["transcript"]
        word_count = info["word_count"]

        # Word count is defined as splitting by whitespace
        actual_word_count = len(transcript.split())
        assert word_count == actual_word_count, (
            f"Word count mismatch for {speaker}. "
            f"Computed {actual_word_count} from transcript, but JSON reports {word_count}."
        )