You are a log analyst investigating a failing data pipeline. An upstream ETL job has been randomly retrying and generating duplicate audit records, which are mysteriously recorded as audio voice-memos containing multi-language metadata (due to an experimental transcription-based logging system). 

Your task is to build a real-time stream-processing and deduplication service.

1. **Audio Artefact Analysis**:
You are provided an audio file at `/app/etl_spikes.wav`. This file contains concatenated voice logs in multiple languages (English, Spanish, and Mandarin).
Write a Python script that extracts the spoken text from this audio file. You must handle Unicode multi-language text processing correctly. Each spoken line represents a log entry. The logs have the format: `[Language Code] [Timestamp] [RecordID] [Status]`. Some records are exact duplicates due to ETL retries.

2. **Deduplication and Transformation**:
Implement a transformation pipeline in Python that:
- Cleans and normalizes the extracted Unicode text.
- Deduplicates the records based on the `RecordID`. If multiple records have the same `RecordID`, keep the one with the earliest `Timestamp`.
- Saves the cleaned, deduplicated logs to a JSON file at `/home/user/processed_logs.json`. The JSON should be an array of objects: `[{"lang": "...", "timestamp": "...", "record_id": "...", "status": "..."}]`.

3. **Query Service (Multi-Protocol)**:
Create and run a gRPC server in Python that exposes the processed logs. 
- Define a protobuf service named `LogAuditor` with an RPC method `GetRecord(RecordRequest) returns (RecordResponse)`.
- The `RecordRequest` should contain a `record_id` (string).
- The `RecordResponse` should return the deduplicated `timestamp`, `status`, and `lang` (strings). If not found, return an empty response.
- The gRPC server MUST listen on exactly `127.0.0.1:50051`.
- The server must run continuously in the background so it can be queried by an external verification test.

To complete this task, write the protobuf definitions, compile them, extract the audio data, process it, output the JSON, and start the gRPC server on the specified port. Leave the server running.