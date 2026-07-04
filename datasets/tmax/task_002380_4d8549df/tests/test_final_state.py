# test_final_state.py

import os
import json
import hashlib
import pytest

def parse_log(log_path):
    valid_records = []
    with open(log_path, 'r') as f:
        content = f.read()

    records = content.split('---')
    for record in records:
        record = record.strip()
        if not record:
            continue

        lines = record.split('\n')
        record_id = None
        status = None

        for line in lines:
            if line.startswith('Record ID:'):
                record_id = line.split(':', 1)[1].strip()
            elif line.startswith('Status:'):
                status = line.split(':', 1)[1].strip()

        if status == 'Valid' and record_id:
            valid_records.append(record_id)

    return valid_records

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_chunks_and_manifest():
    log_path = "/app/metadata/ingest.log"
    manifest_path = "/home/user/manifest.json"
    chunks_dir = "/home/user/chunks"

    assert os.path.exists(log_path), "Ingest log missing."
    valid_records = parse_log(log_path)

    assert os.path.exists(manifest_path), "Manifest file missing."
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    for record_id in valid_records:
        chunk_filename = f"chunk_{record_id}.wav"
        chunk_path = os.path.join(chunks_dir, chunk_filename)

        assert os.path.exists(chunk_path), f"Missing chunk file: {chunk_filename}"

        expected_hash = get_sha256(chunk_path)
        assert chunk_filename in manifest, f"{chunk_filename} missing from manifest."
        assert manifest[chunk_filename] == expected_hash, f"Hash mismatch for {chunk_filename}"

def test_curated_audio():
    curated_path = "/home/user/curated.wav"
    assert os.path.exists(curated_path), "Merged audio file /home/user/curated.wav is missing."
    assert os.path.getsize(curated_path) > 0, "Merged audio file is empty."

def test_transcript():
    transcript_path = "/home/user/transcript.txt"
    assert os.path.exists(transcript_path), "Transcript file missing."

    with open(transcript_path, 'r') as f:
        content = f.read()

    assert len(content.strip()) > 0, "Transcript is empty."
    assert '\n' not in content.strip('\n'), "Transcript should be a single line with no line breaks."