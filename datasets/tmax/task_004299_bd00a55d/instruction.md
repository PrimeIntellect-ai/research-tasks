You are a web developer building a backend feature for a video processing platform. The platform ingests gRPC payloads containing video event logs. You need to build a validator for these logs and extract some baseline metrics from a reference video.

Step 1: Protobuf & Validation Script
We have defined a protobuf schema for the event logs at `/app/schema/video_events.proto`.
```proto
syntax = "proto3";
message Event {
  int64 start_time_ms = 1;
  int64 end_time_ms = 2;
  string event_type = 3;
}
message VideoEventLog {
  repeated Event events = 1;
}
```
Compile this protobuf schema for Python.
Then, write a Python script at `/home/user/validate_logs.py` that takes a single command-line argument (the path to a binary protobuf file containing a `VideoEventLog`). 
The script must read the file and validate the timeline of events. You must ensure the following invariants hold:
- Every event must have `start_time_ms` >= 0.
- Every event must have `start_time_ms` strictly less than `end_time_ms`.
- No two events in the log can overlap in time (if event A ends at time T, event B can start at time T, but they cannot share any inner time span). Note that the events in the repeated field are not guaranteed to be sorted by time.

If the file is completely valid, print `VALID` and exit with code 0.
If the file violates any of the rules, print `INVALID` and exit with code 1.
We have provided training examples in `/app/corpus/clean` (valid logs) and `/app/corpus/evil` (invalid logs) so you can test your script.

Step 2: Video Analysis
We have a reference video artefact located at `/app/reference_video.mp4`.
Using `ffmpeg`, analyze this video to detect the number of black frames using the `blackframe` filter with its default parameters.
Count the total number of frames flagged by this filter and write the exact integer count to a file at `/home/user/black_frames_count.txt`.

Ensure your final `validate_logs.py` script is robust and correctly handles all edge cases.