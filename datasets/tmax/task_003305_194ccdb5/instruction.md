You are an edge computing engineer deploying a new data processing pipeline to a fleet of IoT security devices. These devices stream video and receive configuration payloads remotely. You need to implement a data sanitizer and a video signal analyzer.

Your task has three main components:

1. **Video Signal Analyzer (Rust & FFmpeg)**
There is a diagnostic video file located at `/app/signal_test.mp4`. This video occasionally experiences "signal drops" where the frame goes completely black (average RGB value across the entire frame is strictly less than 15).
You must write a task automation script or use `ffmpeg` combined with Rust to identify the exact frame indices (0-indexed) where these signal drops occur. 
Output the detected frame indices, one per line, to `/home/user/dropouts.txt`.

2. **Adversarial Payload Sanitizer (Rust)**
The IoT devices receive JSON configuration payloads. Malicious actors are attempting to exploit the edge devices using path traversal and command injection inside the JSON payloads.
Write a Rust program at `/home/user/edge_filter/` (initialize it with `cargo init`) that acts as a binary validator.
The compiled binary must take a single file path as a CLI argument: `./target/release/edge_filter <path_to_json>`.
The JSON files have the following structure:
```json
{
  "device_id": "cam-42",
  "target_path": "/var/spool/data",
  "sync_interval": 60
}
```
Your Rust program must parse the JSON. It must REJECT the file (exit with status code `1`) if the `"target_path"` contains any of the following dangerous substrings:
- `../` (Path traversal)
- `$(` (Command substitution)
- `` ` `` (Backtick command injection)
- `&&` or `||` (Shell logical operators)
If the JSON is valid and none of the dangerous substrings are present in `"target_path"`, the program must ACCEPT the file (exit with status code `0`).

3. **Idempotent Deployment Script**
Write a bash script at `/home/user/deploy.sh` that:
- Builds your Rust project in release mode.
- Iterates over all files in `/app/corpora/clean/` and verifies your binary accepts them all (exit code 0).
- Iterates over all files in `/app/corpora/evil/` and verifies your binary rejects them all (exit code 1).
- Runs the video frame extraction and populates `/home/user/dropouts.txt`.
Your deployment script should be idempotent and exit with status code `0` if all checks pass, and `1` if any check fails.

Constraints:
- You may use standard tools like `ffmpeg`, `jq`, and standard Rust crates (e.g., `serde`, `serde_json`).
- Assume standard Linux environment. Do not use root/sudo.