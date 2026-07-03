You are a data engineer tasked with fixing a broken ETL pipeline. The pipeline processes customer service logs containing multi-language transcripts and audio recordings. Due to a bug in the upstream retry logic, the pipeline frequently produces duplicate records, some of which are slightly mangled or contain anomalous changepoints in the text encoding. 

Your objective is to write a Rust command-line tool that acts as a strict ETL filter and sanitiser.

Here are your specific requirements:
1. **Rust CLI Tool**: Create a Rust application at `/home/user/etl_filter`. It must compile with standard Cargo commands.
2. **Audio Processing**: The pipeline provides a diagnostic audio file at `/app/diagnostic_signal.wav`. Your Rust tool must read this audio file, detect the average amplitude of the first 500 milliseconds, and interpolate any missing samples using linear interpolation. The calculated average amplitude (rounded to two decimal places) must be logged to `/home/user/audio_baseline.txt`.
3. **Data Sanitization**: The tool must accept a directory path as an argument. It will iterate over all JSON files in the directory. Each JSON file represents a batch of records.
   - A record has `id`, `timestamp`, `text` (multi-language Unicode), and `retry_count`.
   - Your tool must identify and reject (filter out) records that are duplicates. A record is an adversarial duplicate if it shares the same `id` but has an anomalous character insertion (e.g., a zero-width space or a mismatched Unicode normalization form) compared to the first seen valid record.
   - Valid records must be written out to a `sanitized/` subdirectory within the input directory, preserving the original JSON structure.
4. **Invocation**: Your tool must be callable as: `cargo run --release -- --input-dir <directory>`

Ensure your anomaly detection logic correctly handles Unicode normalization (NFC vs NFD) and detects sudden changepoints in text density.