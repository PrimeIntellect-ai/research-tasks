You are a data engineer tasked with building a Rust-based ETL pipeline that processes video footage and filters incoming metadata payloads from edge devices.

Your objectives:

1. **Video Processing & Aggregation**:
   There is a video file located at `/app/drone_footage.mp4`. 
   Use `ffmpeg` to extract the scene change scores (e.g., using the `select='gt(scene,0)'` or similar frame difference metrics) and insert the frame number, timestamp, and scene score into an SQLite database at `/home/user/pipeline.db`.
   Write a Rust CLI tool in `/home/user/etl_tool` that connects to this SQLite database. 
   Implement a command `cargo run --bin etl_tool -- aggregate` that executes a complex SQL query (using CTEs and Window Functions) to find the 3 longest continuous segments of video (in seconds) where no scene change score exceeded 0.1. Output the result to `/home/user/summary.json` as a JSON array of objects `[{"start_ts": ..., "end_ts": ..., "duration": ...}, ...]`.

2. **Payload Sanitizer**:
   The edge devices send JSON payloads containing metadata, but some devices have been compromised and send malicious SQL injection payloads or malformed schema structures.
   Add a command to your Rust tool: `cargo run --bin etl_tool -- sanitize <file_path>`.
   This command must read the JSON file at `<file_path>`. It should print `ACCEPT` to STDOUT if the payload is valid, and `REJECT` if it contains forbidden SQL keywords (like `DROP`, `UNION`, `OR 1=1`) in any string value, or if the JSON depth exceeds 3 levels.
   
Ensure your Rust application compiles and correctly handles the pipeline tasks. We will test your `sanitize` command against a hidden corpus of clean and evil payloads.