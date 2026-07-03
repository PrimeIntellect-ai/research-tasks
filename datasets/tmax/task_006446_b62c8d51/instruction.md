You are a localization engineer tasked with preparing a messy, multi-lingual video transcription log for a new translation pipeline. The raw log file contains inconsistent timestamps, metadata tags, duplicated lines from a faulty transcription service, and mixed Unicode formats.

The raw log file is located at `/home/user/raw_transcript.log`.

Your objective is to write and execute a Rust program that processes this file and outputs a clean JSON array to `/home/user/clean_transcript.json`.

Here are the strict processing rules your Rust program must follow:

1. **Timestamp Alignment & Parsing:** 
   Each line starts with a timestamp in brackets, either in the format `[YYYY-MM-DD hh:mm:ss]` or just `[hh:mm:ss]`. 
   - If the date is missing, assume it is `2023-11-01`. 
   - Extract and align all timestamps to the UTC ISO 8601 format: `YYYY-MM-DDThh:mm:ssZ`.

2. **Cleaning & Normalization:**
   - After extracting the timestamp, remove any speaker tags formatted as `<some_text>` and any event tags formatted as `[some_text]` from the rest of the line.
   - Trim any leading, trailing, or excessive internal whitespace (e.g., double spaces should be single spaces, though trimming ends is the priority).
   - Normalize the remaining text to Unicode Normalization Form C (NFC).
   - If the cleaned text is empty, drop the line entirely.

3. **Deduplication:**
   - The transcription service often stutters. If the cleaned text of a line is exactly identical to the cleaned text of the *most recently kept* line, drop it. (Do not keep consecutive duplicate texts).

4. **Feature Extraction:**
   - For each valid, deduplicated line, calculate the `char_count`, which is the total number of Unicode scalar values (characters) in the cleaned string.

5. **Output Format:**
   The output at `/home/user/clean_transcript.json` must be a valid JSON array of objects. Each object must have exactly three keys:
   - `"timestamp"`: The ISO 8601 string.
   - `"text"`: The cleaned, NFC-normalized string.
   - `"char_count"`: The integer character count.

You may use standard Rust crates (like `regex`, `chrono`, `serde`, `serde_json`, `unicode-normalization`). Create your Rust project in `/home/user/transcript_parser`.