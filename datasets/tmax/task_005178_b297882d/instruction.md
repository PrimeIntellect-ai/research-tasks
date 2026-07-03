You are tasked with recovering the configuration drift history of a legacy control node. The node's primary audit log was partially corrupted, and our only backup of the high-level state transitions is a screen recording of its diagnostic dashboard (`/app/config_dashboard.mp4`).

Your objective is to extract the configuration checkpoints from the video, interpolate missing data, correlate them with a massive raw event stream, and compute the configuration drift over time.

Step 1: Video Analysis and Imputation
Extract frames from `/app/config_dashboard.mp4`. The video displays diagnostic text in the format `TS: <unix_timestamp> | HASH: <8-char-hex>`. 
Due to transmission errors, some frames are completely black (corrupted). 
Extract the valid timestamps and hashes (you may install `tesseract-ocr` and `pytesseract`). 
For the corrupted frames where timestamps are missing, linearly interpolate the UNIX timestamps based on the preceding and succeeding valid timestamps, rounding to the nearest integer.

Step 2: Large-File Streaming and Alignment
You are provided with a large raw log file at `/app/agent_logs.jsonl`. This file contains millions of system events.
For each timestamp (both extracted and interpolated) from the video, find the exact matching event in `/app/agent_logs.jsonl` where `"timestamp": <unix_timestamp>` and `"event_type": "config_commit"`. 
You must stream this file efficiently, as it is too large to load into memory entirely.

Step 3: Tokenization, Normalization, and Similarity
For each matched event, extract the `"config_payload"` string. 
Normalize this payload by:
1. Converting it to lowercase.
2. Removing all punctuation except underscores.
3. Tokenizing it by whitespace.
4. Sorting the tokens alphabetically.

Compute the Jaccard similarity index between the normalized token set of the *current* timestamp and the *previous* timestamp. (For the first timestamp, the similarity is exactly 1.0).
Configuration drift is defined as `1.0 - Jaccard_similarity`.

Step 4: Output
Generate a final report at `/home/user/drift_report.json` with the following exact structure:
```json
[
  {
    "timestamp": 1698364800,
    "hash": "a1b2c3d4",
    "drift_score": 0.0
  },
  {
    "timestamp": 1698364810,
    "hash": "unknown_due_to_corruption",
    "drift_score": 0.452
  }
]
```
For missing hashes from corrupted frames, set the hash to `"unknown"`.
Round `drift_score` to 3 decimal places.

Your solution must be robust, primarily written in Python, and handle the data pipeline efficiently.