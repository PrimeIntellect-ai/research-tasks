You are a DevOps engineer troubleshooting a data processing pipeline that extracts telemetry from video recordings of server dashboard monitors. 

In `/home/user/video_pipeline/`, there is a Go application (`main.go`) and a helper shell script (`extract_frames.sh`). The pipeline is supposed to read a video file, extract frames, calculate the average grayscale brightness of each frame, and output the results as a JSON array of objects: `[{"frame": 0, "brightness": 45.2}, ...]`.

However, the pipeline has several severe issues:
1. **Filename Handling:** The `extract_frames.sh` script breaks when processing video files with spaces in their names.
2. **Encoding/Serialization Issues:** The Go program periodically crashes with JSON marshaling/unmarshaling errors. The intermediate logs extracted from the video metadata occasionally contain invalid UTF-8 characters and `NaN` float values that break standard serialization.
3. **Performance Bottleneck:** The current Go implementation processes frames sequentially by shelling out to `ffmpeg` and `ImageMagick` for every single frame, making it incredibly slow.
4. **Intermittent Race Condition:** A rudimentary attempt at concurrency in the `processVideoAsync` function contains a data race that intermittently corrupts the output slice.

Your objective:
1. Debug and fix `extract_frames.sh` so it safely handles paths with spaces.
2. Fix the JSON serialization issues in `main.go` so it gracefully handles invalid UTF-8 and sanitizes `NaN` values to `0.0`.
3. Fix the concurrency bugs (race conditions) to ensure the output slice is thread-safe and deterministic.
4. Optimize the frame processing logic to drastically improve throughput. You must refactor the Go code to process the video efficiently (e.g., using bulk frame extraction or efficient ffmpeg filter chains rather than per-frame sub-processes).

There is an incident recording located at `/app/incident_recording.mp4`.
Run your fixed and optimized Go pipeline on this video:
```bash
cd /home/user/video_pipeline
go run main.go --input "/app/incident_recording.mp4" --output "/home/user/final_metrics.json"
```

The file `/home/user/final_metrics.json` must contain the strictly ordered, valid JSON array of the extracted brightness metrics for every frame.