# test_final_state.py

import os
import string
import difflib

def calculate_similarity(file_path, ground_truth):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            prediction = f.read().lower().strip()

        # Remove punctuation for fair comparison
        prediction = prediction.translate(str.maketrans('', '', string.punctuation))
        truth = ground_truth.translate(str.maketrans('', '', string.punctuation))

        # Calculate sequence matcher ratio
        similarity = difflib.SequenceMatcher(None, prediction.split(), truth.split()).ratio()
        return similarity
    except FileNotFoundError:
        return 0.0

def test_transcript_similarity():
    target_path = "/home/user/transcript.txt"
    assert os.path.isfile(target_path), f"Target transcript file {target_path} does not exist."

    truth_text = "the server infrastructure migration is scheduled for next tuesday at midnight ensure all database backups are verified before initiating the sequence"

    score = calculate_similarity(target_path, truth_text)
    threshold = 0.85

    assert score >= threshold, f"Transcription similarity score {score:.4f} is below the required threshold of {threshold:.4f}."