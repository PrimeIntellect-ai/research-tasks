You are an automation specialist tasked with fixing a broken stream processing ETL workflow. 

We have a dashcam telemetry recording located at `/app/telemetry_stream.mp4`. This video contains a subtitle track (Stream #0:1) which acts as a raw telemetry log feed. Due to upstream system glitches and retry mechanisms in our ETL pipeline, the raw logs often contain duplicate event bursts.

Your task has two parts:

Part 1: Extraction
Use `ffmpeg` to extract the subtitle track from `/app/telemetry_stream.mp4` and save it as a raw text file at `/home/user/extracted_logs.srt`. Then, write a quick one-liner to strip out the SRT sequence numbers, timestamps, and empty lines so you are left with just the raw data lines, saving the clean text to `/home/user/raw_telemetry.txt`. 

Part 2: The ETL Processor Script
Write a bash script at `/home/user/process_telemetry.sh` that reads raw telemetry lines from standard input (`stdin`) and prints the processed lines to standard output (`stdout`). 

The raw lines follow this tokenized format:
`TimestampEpochMs|EventType|LicensePlate|Speed`

Your script must perform the following transformations in a deterministic, bit-exact manner:
1. **Normalization**: Convert the `TimestampEpochMs` (which is in milliseconds) into an ISO 8601 UTC formatted string (e.g., `YYYY-MM-DDThh:mm:ssZ`). Fractional seconds should be truncated/ignored.
2. **Data Masking (Anonymization)**: If the `LicensePlate` field matches the exact standard format of three uppercase letters followed by three digits (e.g., `ABC123`), mask the letters with asterisks (e.g., `***123`). If it does not match this exact pattern, leave it unchanged.
3. **Windowed Deduplication**: Due to ETL retry loops, duplicate records are injected. A record is considered a duplicate if it has the *exact same* `EventType` and unmasked `LicensePlate` as a previous record, AND its `TimestampEpochMs` is strictly within 3000 milliseconds (inclusive) of that previous record's timestamp. You must drop these duplicates, keeping only the *first* instance of the record in the stream.
4. **Parallel Processing Compatibility**: Your script must be strictly written in Bash or standard GNU coreutils/awk (no Python, Perl, or Ruby) and handle standard input efficiently.

The output format printed to standard output must be:
`ISO8601Timestamp|EventType|MaskedLicensePlate|Speed`

Make sure the script is executable (`chmod +x /home/user/process_telemetry.sh`). Automated verification will fuzz your script with hundreds of randomly generated telemetry streams to ensure bit-exact parity with our reference implementation.