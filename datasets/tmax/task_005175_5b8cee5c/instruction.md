You are a data scientist tasked with cleaning and smoothing a corrupted telemetry dataset using a specific calibration window.

Your task has two parts:
Part 1: Calibration Video Analysis
We have a calibration video located at `/app/calibration.mp4`. The video flashes a solid white frame periodically.
You must extract the frames of this video and count the exact number of times a fully white frame appears. 
Let this count be `W`. This integer represents our rolling window size for the telemetry data.

Part 2: Telemetry Processor Implementation
Write a Python script at `/home/user/process_telemetry.py` that acts as a Unix pipeline tool.
It should read messy, unstructured log text from standard input (`stdin`) until EOF, extract the data, and output cleaned JSON to standard output (`stdout`).

The input text will contain random logs, but you only care about substrings matching this exact format:
`[DATA] <ISO8601_TIMESTAMP> v=<integer>`
(e.g., `[DATA] 2023-10-01T12:00:05Z v=42`)

Your script must:
1. Extract all valid data points from the input stream. Note that multiple data points might appear on a single line, or be buried inside other text.
2. Sort the extracted data points strictly chronologically by the timestamp.
3. Compute a simple moving average (SMA) for the values using a rolling window of size `W` (the count from Part 1). The window should include the current point and the `W-1` previous points. For the first `k` points where `k < W`, compute the average of all available points up to that point.
4. Output a single JSON array of objects to `stdout`. Each object must have the keys `"t"` (the timestamp string) and `"v_smooth"` (the moving average as a float, rounded to exactly 1 decimal place).

Example Output Format:
```json
[
  {"t": "2023-10-01T12:00:01Z", "v_smooth": 10.0},
  {"t": "2023-10-01T12:00:05Z", "v_smooth": 15.5}
]
```

Ensure your script is robust and efficiently processes the text. Do not hardcode the input data; we will test your script by piping thousands of randomly generated log files into it to verify its output exactly matches our reference implementation.