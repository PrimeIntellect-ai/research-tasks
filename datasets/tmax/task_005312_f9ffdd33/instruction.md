I am building a web feature that processes user-uploaded video payloads along with attached metadata events. I need you to implement a pipeline that extracts specific frames from a video, parses a proprietary state machine format to process events, and creates a strict sanitiser for the incoming metadata.

Here are the requirements:

1. **State Machine & Parser**: There is a proprietary event log format called `.sml` (State Machine Log) located in `/home/user/events.sml`. You must write a parser in Python or Node.js that reads this file. The file dictates a state machine with states `INIT`, `RECORDING`, `PAUSED`, and `STOPPED`. The file format has lines like `STATE_CHANGE:RECORDING timestamp=00:00:05.500`. 
2. **Video Processing**: A video file is located at `/app/fixture.mp4`. Using `ffmpeg`, extract frames only during the `RECORDING` state as defined by the parsed `.sml` file. Save the extracted frames in `/home/user/frames/` as `frame_%04d.jpg` at 1 fps.
3. **Metadata Sanitiser**: Users submit JSON metadata with their videos. I have provided a corpus of valid ("clean") metadata in `/home/user/metadata/clean/` and malicious/invalid ("evil") metadata in `/home/user/metadata/evil/`. You must write a script `/home/user/sanitiser.py` that takes a directory path as an argument, evaluates all JSON files in it, and prints the filename followed by `PASS` or `FAIL`. It must output `FAIL` for 100% of the evil corpus and `PASS` for 100% of the clean corpus. Evil metadata contains embedded XSS payloads, SQL injection attempts, or malformed nested JSON objects exceeding depth 3.
4. **CI/CD & Benchmarking**: Write a shell script at `/home/user/ci_pipeline.sh` that:
   - Runs the sanitiser against both corpora and asserts the expected pass/fail rates.
   - Runs the video processing script.
   - Benchmarks the video processing script using `time` (or similar) and outputs the results to `/home/user/benchmark.log`.

Make sure all output paths and scripts match exactly as requested.