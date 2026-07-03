I need you to build a Go-based ETL data cleaning service that processes audio transcriptions and deduplicates corrupted CSV records. 

Here is the situation:
We have an automated pipeline that failed during retries, resulting in a corrupted CSV file at `/home/user/data/historical_records.csv`. The retries created near-duplicate records with slight typos due to OCR/transcription variations. Also, we just received a new customer support audio recording located at `/app/call_recording.wav`.

Your task:
1. **Transcribe & Extract**: Recover the spoken content from `/app/call_recording.wav` using any suitable command-line tool (you may install tools like `whisper.cpp` or use available ffmpeg pipelines). Extract the structured information from the spoken text: "Customer Name", "Account ID", and "Reported Issue".
2. **Deduplication Engine (Go)**: Write a Go program that reads `/home/user/data/historical_records.csv`. It must implement a string similarity algorithm (like Levenshtein distance) to group and deduplicate records where the "Reported Issue" and "Customer Name" are extremely similar (distance <= 3). 
3. **Merge**: Append the newly extracted record from the audio file into the deduplicated dataset. Log the exact number of duplicates removed to `/home/user/pipeline.log` in the format: `[INFO] Removed X duplicate records.`
4. **Data Service**: The Go program must then spin up an HTTP server listening on `127.0.0.1:8080`. 
    - Endpoint: `GET /api/records?account_id=<ID>`
    - It must return the structured record as JSON.
    - It must require an `Authorization: Bearer secret-agent-token` header. Return 401 Unauthorized otherwise.

Write all necessary Go code, shell scripts, and setups. Leave the HTTP service running in the background. Ensure the Go code handles missing fields gracefully.