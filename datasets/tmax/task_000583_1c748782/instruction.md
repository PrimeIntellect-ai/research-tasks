You are an automation specialist tasked with digitizing legacy sensor data. We have an old industrial pressure system that only outputs its status to a diagnostic display. We captured a 60-second video of this display, located at `/app/sensor_feed.mp4`.

Your goal is to build a multi-stage data processing pipeline in **Go** that extracts this data, handles OCR errors, and resamples the time series.

Here is what you need to do:
1. **Frame Extraction**: Extract frames from the video at 1 frame per second. (You may use `ffmpeg`, which is installed).
2. **OCR Integration**: Use `tesseract` (installed on the system) to read the text from each frame. 
3. **Information Extraction**: The display shows text like:
   ```
   SYSTEM MONITOR v1.0
   Timestamp: 2024-05-01T12:00:05Z
   Pressure: 104.2 kPa
   ```
   Parse the timestamp (ISO8601) and the numerical pressure value. The video contains artificial glitches, so some frames will yield garbage text or be completely unparseable.
4. **Gap-Filling & Resampling**: Determine the earliest and latest valid timestamps extracted. Create a continuous timeline with exactly 1-second intervals between these two bounds. For timestamps where the OCR failed or the frame was corrupted, use **linear interpolation** to estimate the missing pressure values based on the nearest valid data points before and after the gap.
5. **Output**: Save the cleaned, gap-filled time series to a CSV file at `/home/user/interpolated_pressure.csv`. 
   - The CSV must have exactly two columns with headers: `timestamp` and `pressure`.
   - The timestamp must be in ISO8601 format (e.g., `2024-05-01T12:00:05Z`).
   - The pressure must be formatted to 1 decimal place.

Your solution should be robustly orchestrated using Go (shell scripts can be used to wrap ffmpeg/tesseract, but the core alignment, parsing, and gap-filling logic must be in Go). Your final CSV will be evaluated against the ground truth using Mean Squared Error (MSE) on the pressure values.