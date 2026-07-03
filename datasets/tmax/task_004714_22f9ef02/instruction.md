You are an automation specialist tasked with creating a data pipeline that merges legacy system alerts from an old audio dictation tape and a corrupted binary log file.

Your objective is to extract specific "Alert Codes", deduplicate them, and output their cryptographic hashes.

**Step 1: Audio Transcription**
You have been provided with an audio recording of a system administrator dictating alerts at `/app/recording.wav`. 
- Transcribe the English audio. You may install and use any Python libraries you need (e.g., `openai-whisper` using the `tiny.en` model). 
- Extract all "Alert Codes" from the transcription. An Alert Code strictly follows the format: three uppercase letters, a hyphen, and exactly four digits (e.g., `SYS-0492`, `ERR-1029`).

**Step 2: Binary Log Decoding**
You also have a legacy log file at `/app/legacy_logs.bin`. 
- This file contains raw byte streams with mixed character encodings (a mix of UTF-8 and UTF-16LE) and some corrupted/invalid bytes.
- Write a Python script to read this file, robustly handling decoding errors (e.g., by ignoring or replacing invalid characters) to recover as much text as possible.
- Extract all Alert Codes from the decoded text using the same regex pattern.

**Step 3: Hash-Based Deduplication**
- Combine the Alert Codes extracted from both the audio transcription and the binary log.
- Normalize all extracted codes to uppercase.
- You will likely have duplicate codes. Deduplicate them.
- For each unique Alert Code, compute its SHA-256 hash (encode the string as UTF-8 before hashing).

**Output Specification:**
Write the final, deduplicated SHA-256 hashes to a text file at `/home/user/unique_alert_hashes.txt`.
- The file must contain exactly one hash per line.
- The hashes must be sorted in alphabetical order.
- Do not include the original Alert Codes in this file.

Your solution will be evaluated based on the Jaccard similarity between your output hashes and the hidden ground-truth hashes.