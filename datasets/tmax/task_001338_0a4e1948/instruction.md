I am migrating our legacy video analysis pipeline from Python 2 to Python 3, but the entire stack is currently broken. The system consists of a Go-based video frame processor that calls a C++ library, and a Python script that filters the output. 

Here is what you need to do:

1. **Fix the C++ Memory Safety Issue**:
   The C++ library at `/workspace/src/lib/analyzer.cpp` calculates the average brightness of an RGB frame. However, it regularly segfaults due to a memory safety issue (undefined behavior) when iterating over the pixel buffer. Find and fix the memory bug so it safely computes the brightness.

2. **Fix the Go Concurrency Bug**:
   The Go program at `/workspace/src/main.go` extracts frames from `/app/test_run.mp4` using `ffmpeg`, reads them into memory, and dispatches them to the C++ library using goroutines. It is supposed to count the total number of "bright" frames (average brightness > 128). However, there is a race condition in how it increments the `BrightFrameCount` variable, leading to inconsistent results. Fix the concurrency bug. Build the fixed Go binary to `/workspace/bin/processor`. Run it to get the correct `BrightFrameCount`.

3. **Migrate and Implement the Python Filter (Adversarial Corpus)**:
   We have a legacy Python 2 script at `/workspace/legacy_filter.py` that processes frame metadata JSONs. 
   - Migrate this script to Python 3 and save it as `/workspace/filter.py`.
   - Update the `is_clean_record(json_data, calibration_key)` function. The `calibration_key` is the `BrightFrameCount` you obtained from the Go program. 
   - A JSON record is considered "evil" (and must be rejected) if its `signature` field does not equal `(json_data["event_id"] * calibration_key) % 99991`.
   - Furthermore, the old script uses `yaml.load()` which is unsafe. Update it to parse safely and ignore any files that contain malicious payload strings or invalid unicode.
   - The script must expose a CLI: `python3 /workspace/filter.py --input <input_dir> --output <output_dir> --key <calibration_key>`. It should read all `.json` files in `<input_dir>`, evaluate them, and only write the clean ones to `<output_dir>`.

Your final deliverable must successfully compile, run without memory errors or race conditions, and accurately filter a mixture of clean and malicious JSON payloads.