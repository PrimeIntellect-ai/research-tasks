You have inherited an incomplete, undocumented data processing pipeline for an edge telemetry service. The previous developer left suddenly, leaving behind a corrupted database, unprocessed audio, and a broken data sanitization module.

Your objective is to recover the system state, process the lingering artifacts, and fix the security filter. 

**Step 1: Audio Transcription**
An unprocessed emergency audio transmission was left in `/app/audio/distress_signal.wav`. You must transcribe this audio file. You may install any necessary open-source CLI tools or Python libraries (e.g., `whisper`, `ffmpeg`) to accomplish this. 

**Step 2: Database Recovery & Timeline Reconstruction**
The primary telemetry database crashed. In `/app/db/`, you will find:
- `sys_service.log`: Interleaved, unsorted application logs.
- `telemetry.wal`: A Write-Ahead Log containing the last few unprocessed transactions.
Reconstruct the correct chronological sequence of events by correlating the timestamps in `sys_service.log` with the transaction IDs in `telemetry.wal`. 

**Step 3: Fix the Rust Log Sanitizer (Adversarial Challenge)**
The service uses a Rust-based CLI tool at `/app/pii-filter` to sanitize logs before they are written to the database. Currently, it allows malicious payloads and Personally Identifiable Information (PII) to pass through. 
You must modify `/app/pii-filter/src/main.rs` so that it reads a file path provided as its first command-line argument, analyzes the text, and exits with:
- **Exit code 0** if the file is completely clean.
- **Exit code 1** if the file contains any "evil" content (e.g., SSNs in `XXX-XX-XXXX` format, AWS-style API keys starting with `AKIA`, or format string vulnerabilities like `%x%x%x`).

You will be graded against a hidden adversarial corpus. Your solution must reject 100% of the "evil" files and preserve/accept 100% of the "clean" files.

**Step 4: Final Integration**
Create a final JSON report at `/home/user/recovery_report.json` with exactly this structure:
```json
{
  "transcription": "<exact transcribed text of the audio file, lowercase>",
  "crash_timestamp": "<the exact ISO8601 timestamp of the FATAL crash event found in the logs>",
  "last_recovered_tx_id": "<the highest transaction ID successfully parsed from the WAL before the crash>"
}
```