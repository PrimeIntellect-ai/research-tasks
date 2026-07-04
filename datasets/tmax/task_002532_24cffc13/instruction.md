You are an automation specialist at an industrial manufacturing plant. You need to create a multi-stage data processing workflow that extracts metrics from visual logs and validates incoming tabular sensor data. 

**Part 1: Visual Time-Series Extraction**
You have been provided with a diagnostic video of a conveyor belt process located at `/app/conveyor_belt.mp4`. Every time a machine cycle completes, a bright red indicator light flashes.
1. Extract the frames of this video.
2. Calculate a simple summary statistic for each frame to detect the red flashes: a frame is considered part of a "cycle flash" if its average Red pixel value minus its average Blue pixel value is strictly greater than 50.0 (i.e., `mean(R) - mean(B) > 50.0`).
3. Sort and group these detections to find the exact frame indices where the flashes occur.
4. Output your results to a JSON file at `/home/user/cycle_frames.json` with exactly this format:
```json
{
  "cycle_frames": [12, 13, 14, 88, 89, 150]
}
```
*(Ensure the frame indices are 0-indexed integers, matching standard ffmpeg / OpenCV extraction order).*

**Part 2: Time-Series Quality Gate (Adversarial Validation)**
External sensor stations upload telemetry as CSV files. You must implement a constraint-based data validation checkpoint to reject malformed or anomalous data.
Create a Python script at `/home/user/quality_gate.py` that acts as a classifier. 

It must accept a single command-line argument (the path to a CSV file) and output exactly the word `ACCEPT` or `REJECT` to standard output.

To be ACCEPTED, the CSV must meet *all* the following constraints:
1. **Headers**: The first row must exactly be `timestamp_ms,sensor_A,sensor_B`.
2. **Monotonicity**: `timestamp_ms` (integers) must be strictly monotonically increasing.
3. **Continuity**: There must be no gaps strictly greater than `1000` milliseconds between consecutive `timestamp_ms` readings.
4. **Local Aggregation**: The rolling 3-sample average of `sensor_A` (i.e., the mean of the current row and the two immediately preceding rows) must never exceed `100.0`. (The first two rows are exempt from this specific check since they lack 2 preceding rows).
5. **Global Statistics**: `sensor_B` must contain valid floats, and its global mean across the entire file must be exactly within the inclusive range `[10.0, 20.0]`.

Any file failing one or more constraints must be REJECTED. The automated verifier will run your script against an extensive suite of hidden "clean" files and "evil" files that subtly violate these rules. Your classifier must be perfectly accurate.