You are a data engineer tasked with building an automated ETL pipeline that processes field operator logs and raw telemetry data.

We have received an audio recording from a field operator detailing specific machine IDs that are exhibiting anomalous behavior. We also have a raw, messy telemetry export.

Your task:
1. **Audio Extraction**: An audio file is located at `/app/anomalies.wav`. Transcribe this audio to recover the spoken machine IDs. The operator uses phonetic alphabet and standard numbers (e.g., "Alpha seven three bravo" -> `A73B`).
2. **Data Cleaning & Filtering**: Read the raw telemetry data from `/app/telemetry.csv`. 
   - This file contains records from many machines, but you only care about the anomalous machines identified in the audio.
   - The CSV file has mixed character encodings (some lines are valid UTF-8, others are Windows-1252/ISO-8859-1). You must normalize all extracted data to pure UTF-8.
   - The columns are `timestamp,machine_id,temperature,sensor_reading,status_notes`.
3. **Validation & Deduplication**:
   - Discard any records where the `temperature` is not a valid float, or falls outside the range -50.0 to 150.0.
   - Deduplicate the records. Two records are considered duplicates if the SHA-256 hash of the concatenated string `timestamp` + `machine_id` are identical. Keep only the first occurrence you encounter.
4. **Data Serving**:
   - Create and run an HTTP server listening exactly on `127.0.0.1:8080`.
   - The server must handle `GET /api/v1/anomalies?id=<machine_id>` requests.
   - For a given `machine_id`, it must return a JSON response with status 200 containing a JSON array of objects representing the cleaned records for that machine, ordered chronologically by `timestamp`.
   - Keys in the JSON objects should strictly be: `timestamp`, `machine_id`, `temperature`, `sensor_reading`, `status_notes`.

Ensure your HTTP service is running in the background or foreground so it can answer requests indefinitely. You can use standard CLI tools, Python, or any combination thereof. Standard audio processing libraries (like `openai-whisper` or `SpeechRecognition`) can be installed via pip.

The verification process will connect to `http://127.0.0.1:8080` and issue requests for the specific anomalous IDs, verifying the JSON structure and the precise filtered/deduplicated data.