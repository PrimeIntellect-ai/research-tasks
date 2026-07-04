You are a data engineer tasked with building a robust ETL pipeline to analyze customer service audio logs. 

We have a raw audio recording of a customer support call located at `/app/call_recording.wav`. Your goal is to extract the spoken words, align them into precise time buckets, and aggregate word frequencies using Go.

Here is your workflow:
1. **Transcription**: Extract the text and timestamps from `/app/call_recording.wav`. You may use `ffmpeg` and any available command-line transcription tools (like whisper.cpp, which you can download and compile if not present, or use any standard Linux tool to generate an SRT/VTT file). 
2. **Data Processing (Go)**: Write a Go application at `/home/user/etl/process.go` that:
   - Streams the generated transcript file (avoid loading the entire file into memory at once).
   - Parses the timestamps and aligns the text into **10-second time buckets** (e.g., `0-10`, `10-20`, `20-30`). Time is in seconds from the start of the audio.
   - Tokenizes the spoken text within each bucket.
   - Normalizes the tokens: lowercase everything and strip out all non-alphanumeric characters.
   - Aggregates the data to count the frequency of each word per bucket.
3. **Output**: Your Go program must write the results to `/home/user/etl/output.jsonl`. Each line must be a JSON object with the following schema:
   `{"bucket_start": 0, "bucket_end": 10, "word": "hello", "count": 1}`
   `{"bucket_start": 0, "bucket_end": 10, "word": "world", "count": 2}`

Ensure your Go code is compiled and run to produce the final `output.jsonl` file. Your pipeline will be evaluated by an automated verifier that compares your extracted word counts and time buckets against a hidden reference transcript. You do not need to be 100% perfect on transcription, but your time-bucketing, normalization, and aggregation logic in Go must be flawless to achieve a passing overlap score.