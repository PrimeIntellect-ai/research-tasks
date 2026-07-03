I am an automation specialist building a fast audio processing pipeline for an upcoming project. I need you to create a Go-based workflow that processes a large audio file, extracts specific segments, transcribes them concurrently, and aggregates summary statistics.

Here is the setup and requirements:
1. There is an audio file located at `/app/interview.wav` (16kHz, 16-bit WAV).
2. There is a CSV file located at `/app/segments.csv` with the following columns: `SegmentID,StartTime,EndTime,SpeakerID`. (Times are in seconds, e.g., `0.0`, `15.5`).
3. You must use Go to write an orchestration program at `/home/user/pipeline/process.go`.

Your Go program must perform the following tasks:
- **Streaming & Chunking**: Read `/app/segments.csv`. For each row, use `ffmpeg` to extract that exact time window from `/app/interview.wav` into a temporary 16kHz WAV file.
- **Transcription**: Clone the `whisper.cpp` repository (https://github.com/ggerganov/whisper.cpp.git) into `/home/user/whisper.cpp`, compile it (`make`), and download the `tiny.en` model using their provided script (`bash ./models/download-ggml-model.sh tiny.en`). Run the compiled `main` binary on each extracted audio chunk to get the transcript. 
- **Concurrency**: To speed up processing, your Go program must process (extract and transcribe) up to 4 segments concurrently.
- **Aggregation & Output**: Once all segments are processed, aggregate the text by `SpeakerID`. Compute the total word count for each speaker (split by whitespace). 
- Write the final results to `/home/user/pipeline/summary.json` in the exact following format:
```json
{
  "speakers": {
    "Speaker_1": {
      "transcript": "hello world ...",
      "word_count": 42
    },
    "Speaker_2": {
      "transcript": "yes I agree ...",
      "word_count": 15
    }
  }
}
```
*Note: Strip leading/trailing whitespaces from the aggregated transcripts, and join multiple segments from the same speaker with a single space in the order of their `SegmentID`.*

Please implement and run this pipeline. Ensure your Go code handles errors robustly and cleans up any temporary audio chunks.