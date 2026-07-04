Wake up! It's 3:00 AM and you've just been paged. 

Our upstream data ingestion pipeline is sporadically crashing, dropping critical telemetry packets. The ingestion script at `/home/user/processor.py` is failing intermittently with a `ValueError("Fatal parsing error")` when processing certain hex-encoded payloads, but our logging system rotated and we lost the exact input that caused the most recent crash.

However, the system managed to dump the raw memory of the worker process right before it died, saved at `/home/user/worker.dmp`. We suspect line noise corrupted the packet in memory, interspersing invalid characters into the hex stream.

Your task is to isolate the exact byte sequence causing the crash so the development team can patch it in the morning.

Perform the following steps:
1. **Analyze the Memory Dump:** Extract the corrupted payload from `/home/user/worker.dmp`. The payload immediately follows the marker string `CRIT_PAYLOAD_START:` and ends at the first space character.
2. **Recover the Input:** Clean the extracted payload by removing any characters that are NOT valid hexadecimal characters (valid characters are `0-9`, `a-f`, and `A-F`). Save this fully cleaned, contiguous hex string to `/home/user/cleaned_payload.txt`.
3. **Reproduce and Isolate:** The crash is triggered by a specific 4-byte (8 hex character) sequence. Write a short fuzzing/testing script in Python to feed 8-character sliding windows of the cleaned payload (e.g., chars 0-7, 1-8, 2-9) into `/home/user/processor.py` as a command-line argument.
4. **Log the Root Cause:** Once you identify the exact 8-character sequence that causes `/home/user/processor.py` to exit with a non-zero status and print a fatal error, save that 8-character string to `/home/user/crash_chunk.txt`.

Ensure `/home/user/cleaned_payload.txt` and `/home/user/crash_chunk.txt` contain exactly the requested strings with no trailing newlines or extra text.