You are a data scientist building an automated data-cleaning pipeline for a self-driving car project. You have a video feed and a noisy telemetry CSV file that need to be processed, synchronized, and served via an HTTP API.

Write a Rust web service that listens on `127.0.0.1:9000`.

When an HTTP GET request is made to the `/data` endpoint, your service must perform the following pipeline:
1. **Video Processing**: Extract exactly 5 frames from the video located at `/app/video.mp4`, specifically at timestamps `00:00:01`, `00:00:02`, `00:00:03`, `00:00:04`, and `00:00:05`. Scale each frame to exactly 64x64 pixels and output as raw RGB24. 
2. **Hashing**: Compute the SHA-256 hash of the raw RGB24 byte data (exactly 64 * 64 * 3 = 12288 bytes) for each of the 5 frames.
3. **CSV Cleaning**: Read the CSV file at `/app/telemetry.csv`. The CSV has headers `timestamp,value,notes`. Some rows are corrupted and contain embedded newline characters (`\n`) within the quoted `notes` field. Your pipeline must gracefully read the CSV but silently drop any row where the `notes` field contains a newline character. 
4. **Synchronization and Deduplication**: Match each of the 5 frames (t=1,2,3,4,5) with the cleaned CSV row that has the exact corresponding integer `timestamp`. Then, perform deduplication: if multiple consecutive frames share the exact same telemetry `value`, keep only the first occurrence in the sequence.
5. **Response**: Return an HTTP 200 OK with a JSON response containing the final deduplicated sequence. The JSON must be an array of objects, strictly in chronological order, with the format:
```json
[
  {
    "timestamp": 1,
    "frame_hash": "<hex-encoded-sha256>",
    "telemetry_value": <integer-value>
  },
  ...
]
```

Requirements:
- Your Rust project must be created in `/home/user/pipeline_service`.
- You may use `ffmpeg` via the command line (e.g., using `std::process::Command` in Rust) to extract the frames.
- You can use any Rust crates you like (e.g., `axum`, `tokio`, `csv`, `sha2`, `serde_json`).
- Ensure the server stays running in the foreground or background so that it can be tested.

Start the service and leave it listening on port 9000.