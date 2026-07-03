You are a data engineer building an ETL pipeline. We receive audio reports from field agents, which are transcribed into JSON format. 

Part 1:
We have received an audio file located at `/app/field_report.wav`. We have a pre-installed transcription tool at `/usr/local/bin/transcribe` that takes the path to a WAV file and outputs a JSON transcription to stdout. Run this tool on `/app/field_report.wav` and save the raw JSON output to `/home/user/initial_report.json`.

Part 2:
Write a Go program located at `/home/user/etl_processor.go` that reads a stream of JSON records from standard input and writes a validated CSV to standard output. 
The input JSON objects have the following structure:
`{"id": "string", "reported_name": "string", "expected_name": "string", "confidence": float64, "transcript_text": "string"}`

Your Go program must perform the following ETL operations for each record:
1. **Multi-format/Extraction:** Read the JSON from `stdin`.
2. **Constraint Validation:** Discard any record where the `confidence` is less than 0.85 or the `id` is empty.
3. **Similarity Computation:** Compute the Levenshtein distance between `reported_name` and `expected_name`.
4. **Output:** Write to `stdout` a CSV line (without headers) containing: `id,reported_name,expected_name,levenshtein_distance,transcript_length` (where transcript_length is the character count of `transcript_text`).

Build the executable and save it as `/home/user/etl_processor`.
Ensure your Go program precisely matches this behavior, as it will be rigorously fuzzed against thousands of random JSON inputs.